use pyo3::exceptions::PyException;

pyo3::create_exception!(ruff.exceptions, RuffError, PyException);
pyo3::create_exception!(ruff.exceptions, ParseError, RuffError);
pyo3::create_exception!(ruff.exceptions, ConfigError, RuffError);
pyo3::create_exception!(ruff.exceptions, RuleNotFoundError, RuffError);
