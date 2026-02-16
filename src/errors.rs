use pyo3::exceptions::PyException;

pyo3::create_exception!(pyruff.exceptions, RuffError, PyException);
pyo3::create_exception!(pyruff.exceptions, ParseError, RuffError);
pyo3::create_exception!(pyruff.exceptions, ConfigError, RuffError);
pyo3::create_exception!(pyruff.exceptions, RuleNotFoundError, RuffError);
