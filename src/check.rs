use std::path::Path;

use pyo3::prelude::*;
use pyo3::types::PyDict;
use ruff_linter::linter::{lint_fix, lint_only, ParseSource};
use ruff_linter::registry::Rule;
use ruff_linter::rule_selector::{PreviewOptions, RuleSelector};
use ruff_linter::settings::flags::Noqa;
use ruff_linter::settings::rule_table::RuleTable;
use ruff_linter::settings::types::{PreviewMode, UnsafeFixes};
use ruff_linter::settings::LinterSettings;
use ruff_linter::source_kind::SourceKind;
use ruff_linter::FixAvailability;
use ruff_python_ast::PySourceType;

use crate::config;
use crate::errors::{ConfigError, RuffError};

fn parse_selectors(codes: &[String]) -> Vec<RuleSelector> {
    codes
        .iter()
        .filter_map(|code| code.parse::<RuleSelector>().ok())
        .collect()
}

fn resolve_linter_settings(
    config: Option<&str>,
    isolated: bool,
    filename: &str,
) -> PyResult<LinterSettings> {
    if isolated {
        return Ok(LinterSettings::default());
    }

    if let Some(config_path) = config {
        // Explicit config file
        let settings = config::resolve_settings(Some(config_path), None)
            .map_err(|e| ConfigError::new_err(format!("{e}")))?;
        if let Some(s) = settings {
            return Ok(s.linter);
        }
    } else {
        // Auto-discover from filename or CWD
        let anchor = if filename != "<stdin>" {
            Some(filename)
        } else {
            None
        };
        let settings = config::resolve_settings(None, anchor)
            .map_err(|e| ConfigError::new_err(format!("{e}")))?;
        if let Some(s) = settings {
            return Ok(s.linter);
        }
    }

    Ok(LinterSettings::default())
}

fn apply_overrides(
    settings: &mut LinterSettings,
    select: Option<Vec<String>>,
    ignore: Option<Vec<String>>,
    extend_select: Option<Vec<String>>,
    target_version: Option<&str>,
    preview: Option<bool>,
) {
    let preview_mode = match preview {
        Some(true) => PreviewMode::Enabled,
        Some(false) => PreviewMode::Disabled,
        None => settings.preview,
    };
    settings.preview = preview_mode;

    if let Some(ver) = target_version {
        use ruff_linter::settings::TargetVersion;
        use ruff_python_ast::PythonVersion;
        let version = match ver {
            "py37" => Some(PythonVersion::PY37),
            "py38" => Some(PythonVersion::PY38),
            "py39" => Some(PythonVersion::PY39),
            "py310" => Some(PythonVersion::PY310),
            "py311" => Some(PythonVersion::PY311),
            "py312" => Some(PythonVersion::PY312),
            "py313" => Some(PythonVersion::PY313),
            "py314" => Some(PythonVersion::PY314),
            _ => None,
        };
        if let Some(v) = version {
            settings.unresolved_target_version = TargetVersion::from(v);
        }
    }

    let preview_opts = PreviewOptions {
        mode: preview_mode,
        require_explicit: false,
    };

    if let Some(select_codes) = select {
        let selectors = parse_selectors(&select_codes);
        let mut rule_table = RuleTable::empty();
        for selector in &selectors {
            for rule in selector.rules(&preview_opts) {
                rule_table.enable(rule, true);
            }
        }
        settings.rules = rule_table;
    }

    if let Some(extend_codes) = extend_select {
        let selectors = parse_selectors(&extend_codes);
        for selector in &selectors {
            for rule in selector.rules(&preview_opts) {
                settings.rules.enable(rule, true);
            }
        }
    }

    if let Some(ignore_codes) = ignore {
        let selectors = parse_selectors(&ignore_codes);
        for selector in &selectors {
            for rule in selector.rules(&preview_opts) {
                settings.rules.disable(rule);
            }
        }
    }
}

fn diagnostic_to_dict<'py>(
    py: Python<'py>,
    diag: &ruff_db::diagnostic::Diagnostic,
) -> PyResult<Bound<'py, PyDict>> {
    let dict = PyDict::new(py);

    let message = diag.primary_message();
    dict.set_item("message", message)?;

    let code = diag.secondary_code_or_id().to_string();
    dict.set_item("code", &code)?;

    if let Ok(rule) = Rule::from_code(&code) {
        if let Some(url) = rule.url() {
            dict.set_item("url", url)?;
        } else {
            dict.set_item("url", py.None())?;
        }
        let fixable = !matches!(rule.fixable(), FixAvailability::None);
        dict.set_item("fixable", fixable)?;
    } else {
        dict.set_item("url", py.None())?;
        dict.set_item("fixable", false)?;
    }

    Ok(dict)
}

#[pyfunction]
#[pyo3(signature = (
    source,
    *,
    filename="<stdin>",
    config=None,
    isolated=false,
    select=None,
    ignore=None,
    extend_select=None,
    target_version=None,
    preview=None,
    ignore_noqa=false,
))]
#[allow(clippy::too_many_arguments)]
pub fn check_source(
    py: Python<'_>,
    source: &str,
    filename: &str,
    config: Option<&str>,
    isolated: bool,
    select: Option<Vec<String>>,
    ignore: Option<Vec<String>>,
    extend_select: Option<Vec<String>>,
    target_version: Option<&str>,
    preview: Option<bool>,
    ignore_noqa: bool,
) -> PyResult<Vec<Py<PyDict>>> {
    let mut settings = resolve_linter_settings(config, isolated, filename)?;
    apply_overrides(
        &mut settings,
        select,
        ignore,
        extend_select,
        target_version,
        preview,
    );

    let path = Path::new(filename);
    let source_kind = SourceKind::Python {
        code: source.to_string(),
        is_stub: false,
    };
    let source_type = PySourceType::from(path);
    let noqa = if ignore_noqa {
        Noqa::Disabled
    } else {
        Noqa::Enabled
    };

    let result = lint_only(
        path,
        None,
        &settings,
        noqa,
        &source_kind,
        source_type,
        ParseSource::None,
    );

    let mut diagnostics = Vec::new();
    for diag in &result.diagnostics {
        diagnostics.push(diagnostic_to_dict(py, diag)?.unbind());
    }
    Ok(diagnostics)
}

#[pyfunction]
#[pyo3(signature = (
    source,
    *,
    filename="<stdin>",
    config=None,
    isolated=false,
    select=None,
    ignore=None,
    extend_select=None,
    target_version=None,
    preview=None,
    ignore_noqa=false,
    unsafe_fixes=false,
))]
#[allow(clippy::too_many_arguments)]
pub fn fix_source(
    py: Python<'_>,
    source: &str,
    filename: &str,
    config: Option<&str>,
    isolated: bool,
    select: Option<Vec<String>>,
    ignore: Option<Vec<String>>,
    extend_select: Option<Vec<String>>,
    target_version: Option<&str>,
    preview: Option<bool>,
    ignore_noqa: bool,
    unsafe_fixes: bool,
) -> PyResult<Py<PyDict>> {
    let mut settings = resolve_linter_settings(config, isolated, filename)?;
    apply_overrides(
        &mut settings,
        select,
        ignore,
        extend_select,
        target_version,
        preview,
    );

    let path = Path::new(filename);
    let source_kind = SourceKind::Python {
        code: source.to_string(),
        is_stub: false,
    };
    let source_type = PySourceType::from(path);
    let noqa = if ignore_noqa {
        Noqa::Disabled
    } else {
        Noqa::Enabled
    };
    let unsafe_mode = if unsafe_fixes {
        UnsafeFixes::Enabled
    } else {
        UnsafeFixes::Disabled
    };

    let result = lint_fix(
        path,
        None,
        noqa,
        unsafe_mode,
        &settings,
        &source_kind,
        source_type,
    )
    .map_err(|e| RuffError::new_err(format!("{e}")))?;

    let output = result.transformed.source_code().to_string();

    let mut fixed_count: usize = 0;
    for (_code, _name, count) in result.fixed.iter() {
        fixed_count += count;
    }

    let mut remaining_diagnostics: Vec<Py<PyDict>> = Vec::new();
    for diag in &result.result.diagnostics {
        remaining_diagnostics.push(diagnostic_to_dict(py, diag)?.unbind());
    }

    let result_dict = PyDict::new(py);
    result_dict.set_item("output", output)?;
    result_dict.set_item("fixed_count", fixed_count)?;
    result_dict.set_item("remaining", remaining_diagnostics)?;
    Ok(result_dict.unbind())
}
