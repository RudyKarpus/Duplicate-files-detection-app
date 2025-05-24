use pyo3::prelude::*;

#[pyfunction]
fn hash(text: &str) -> PyResult<String> {
    Ok(format!("Hashed: {}", text))
}

#[pymodule]
fn detection_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash, m)?)?;
    Ok(())
}
