use pyo3::prelude::*;
use pyo3::types::PyDict;
use ruff_linter::registry::Rule;
use ruff_linter::FixAvailability;
use strum::IntoEnumIterator;

use crate::errors::RuleNotFoundError;

fn rule_to_dict<'py>(py: Python<'py>, rule: Rule) -> PyResult<Bound<'py, PyDict>> {
    let dict = PyDict::new(py);
    let code = rule.noqa_code().to_string();
    dict.set_item("code", &code)?;
    dict.set_item("name", rule.name().as_str())?;

    let linter = rule_linter_name(&code);
    dict.set_item("linter", linter)?;

    let fixable = !matches!(rule.fixable(), FixAvailability::None);
    dict.set_item("fixable", fixable)?;
    dict.set_item("preview", rule.is_preview())?;

    if let Some(explanation) = rule.explanation() {
        dict.set_item("explanation", explanation)?;
    } else {
        dict.set_item("explanation", py.None())?;
    }

    if let Some(url) = rule.url() {
        dict.set_item("url", url)?;
    } else {
        dict.set_item("url", py.None())?;
    }

    Ok(dict)
}

fn rule_linter_name(code: &str) -> &'static str {
    let prefix: String = code.chars().take_while(|c| c.is_alphabetic()).collect();
    match prefix.as_str() {
        "E" | "W" => "pycodestyle",
        "F" => "Pyflakes",
        "C90" => "mccabe",
        "I" => "isort",
        "N" => "pep8-naming",
        "D" => "pydocstyle",
        "UP" => "pyupgrade",
        "YTT" => "flake8-2020",
        "ANN" => "flake8-annotations",
        "ASYNC" => "flake8-async",
        "S" => "flake8-bandit",
        "BLE" => "flake8-blind-except",
        "FBT" => "flake8-boolean-trap",
        "B" => "flake8-bugbear",
        "A" => "flake8-builtins",
        "COM" => "flake8-commas",
        "CPY" => "flake8-copyright",
        "C4" => "flake8-comprehensions",
        "DTZ" => "flake8-datetimez",
        "T10" => "flake8-debugger",
        "DJ" => "flake8-django",
        "EM" => "flake8-errmsg",
        "EXE" => "flake8-executable",
        "FA" => "flake8-future-annotations",
        "ISC" => "flake8-implicit-str-concat",
        "ICN" => "flake8-import-conventions",
        "LOG" => "flake8-logging",
        "G" => "flake8-logging-format",
        "INP" => "flake8-no-pep420",
        "PIE" => "flake8-pie",
        "T20" => "flake8-print",
        "PYI" => "flake8-pyi",
        "PT" => "flake8-pytest-style",
        "Q" => "flake8-quotes",
        "RSE" => "flake8-raise",
        "RET" => "flake8-return",
        "SLF" => "flake8-self",
        "SLOT" => "flake8-slots",
        "SIM" => "flake8-simplify",
        "TID" => "flake8-tidy-imports",
        "TC" => "flake8-type-checking",
        "INT" => "flake8-gettext",
        "ARG" => "flake8-unused-arguments",
        "PTH" => "flake8-use-pathlib",
        "TD" => "flake8-todos",
        "FIX" => "flake8-fixme",
        "ERA" => "eradicate",
        "PD" => "pandas-vet",
        "PGH" => "pygrep-hooks",
        "PL" | "PLC" | "PLE" | "PLR" | "PLW" => "Pylint",
        "TRY" => "tryceratops",
        "FLY" => "flynt",
        "NPY" => "NumPy-specific rules",
        "FAST" => "FastAPI",
        "AIR" => "Airflow",
        "PERF" => "Perflint",
        "FURB" => "refurb",
        "DOC" => "pydoclint",
        "RUF" => "Ruff-specific rules",
        _ => "unknown",
    }
}

#[pyfunction]
#[pyo3(signature = (*, preview=false))]
pub fn get_rules(py: Python<'_>, preview: bool) -> PyResult<Vec<Py<PyDict>>> {
    let mut results = Vec::new();
    for rule in Rule::iter() {
        if !preview && rule.is_preview() {
            continue;
        }
        let dict = rule_to_dict(py, rule)?;
        results.push(dict.unbind());
    }
    Ok(results)
}

#[pyfunction]
pub fn get_rule(py: Python<'_>, code: &str) -> PyResult<Py<PyDict>> {
    let rule = Rule::from_code(code)
        .map_err(|_| RuleNotFoundError::new_err(format!("Unknown rule code: {code}")))?;
    let dict = rule_to_dict(py, rule)?;
    Ok(dict.unbind())
}
