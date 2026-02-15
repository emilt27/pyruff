use std::path::Path;

use pyo3::prelude::*;
use ruff_python_ast::PythonVersion;
use ruff_python_formatter::{format_module_source, FormatModuleError, PyFormatOptions};

use crate::config;
use crate::errors::{ConfigError, ParseError};

fn convert_format_error(err: FormatModuleError) -> PyErr {
    match err {
        FormatModuleError::ParseError(e) => ParseError::new_err(format!("{e}")),
        FormatModuleError::FormatError(e) => ParseError::new_err(format!("Format error: {e}")),
        FormatModuleError::PrintError(e) => ParseError::new_err(format!("Print error: {e}")),
    }
}

fn parse_python_version(ver: &str) -> Option<PythonVersion> {
    match ver {
        "py37" => Some(PythonVersion::PY37),
        "py38" => Some(PythonVersion::PY38),
        "py39" => Some(PythonVersion::PY39),
        "py310" => Some(PythonVersion::PY310),
        "py311" => Some(PythonVersion::PY311),
        "py312" => Some(PythonVersion::PY312),
        "py313" => Some(PythonVersion::PY313),
        "py314" => Some(PythonVersion::PY314),
        _ => None,
    }
}

fn resolve_format_options(
    filename: &str,
    config_path: Option<&str>,
    isolated: bool,
    line_length: Option<u16>,
    target_version: Option<&str>,
    preview: Option<bool>,
) -> PyResult<PyFormatOptions> {
    let path = Path::new(filename);

    // Start from config-resolved options or defaults
    let mut options = if isolated {
        PyFormatOptions::from_extension(path)
    } else {
        // Try to resolve config
        let anchor = if filename != "<stdin>" {
            Some(filename)
        } else {
            None
        };
        let settings = config::resolve_settings(config_path, anchor)
            .map_err(|e| ConfigError::new_err(format!("{e}")))?;

        if let Some(s) = settings {
            use ruff_python_ast::PySourceType;
            let source_type = PySourceType::from(path);
            s.formatter
                .to_format_options(source_type, filename, Some(path))
        } else {
            PyFormatOptions::from_extension(path)
        }
    };

    // Apply explicit overrides on top
    if let Some(width) = line_length {
        use ruff_formatter::LineWidth;
        if let Ok(lw) = LineWidth::try_from(width) {
            options = options.with_line_width(lw);
        }
    }

    if let Some(p) = preview {
        use ruff_python_formatter::PreviewMode;
        if p {
            options = options.with_preview(PreviewMode::Enabled);
        } else {
            options = options.with_preview(PreviewMode::Disabled);
        }
    }

    if let Some(ver) = target_version {
        if let Some(v) = parse_python_version(ver) {
            options = options.with_target_version(v);
        }
    }

    Ok(options)
}

#[pyfunction]
#[pyo3(signature = (
    source,
    *,
    filename="<stdin>",
    config=None,
    isolated=false,
    line_length=None,
    target_version=None,
    preview=None,
))]
pub fn format_string(
    source: &str,
    filename: &str,
    config: Option<&str>,
    isolated: bool,
    line_length: Option<u16>,
    target_version: Option<&str>,
    preview: Option<bool>,
) -> PyResult<String> {
    let options = resolve_format_options(
        filename,
        config,
        isolated,
        line_length,
        target_version,
        preview,
    )?;
    let printed = format_module_source(source, options).map_err(convert_format_error)?;
    Ok(printed.as_code().to_string())
}
