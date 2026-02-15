use pyo3::prelude::*;

mod check;
mod config;
mod errors;
mod format;
mod rules;

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Format
    m.add_function(wrap_pyfunction!(format::format_string, m)?)?;

    // Check / Fix
    m.add_function(wrap_pyfunction!(check::check_source, m)?)?;
    m.add_function(wrap_pyfunction!(check::fix_source, m)?)?;

    // Rules
    m.add_function(wrap_pyfunction!(rules::get_rules, m)?)?;
    m.add_function(wrap_pyfunction!(rules::get_rule, m)?)?;

    // Exceptions
    m.add("RuffError", m.py().get_type::<errors::RuffError>())?;
    m.add("ParseError", m.py().get_type::<errors::ParseError>())?;
    m.add("ConfigError", m.py().get_type::<errors::ConfigError>())?;
    m.add(
        "RuleNotFoundError",
        m.py().get_type::<errors::RuleNotFoundError>(),
    )?;

    Ok(())
}
