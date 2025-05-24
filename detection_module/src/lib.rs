use pyo3::prelude::*;
use rayon::prelude::*;


#[pyfunction]
fn hash_file(path: String) -> Option<String> {
    Ok(format!("Hashed: {}", text))
}
#[pyfunction]
fn find_duplicates(hashes: Vec<(String, String)>) -> PyResult<Vec<Vec<String>>> {
}

#[pymodule]
fn detection_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash, m)?)?;
    m.add_function(wrap_pyfunction!(find_duplicates, m)?)?;
    Ok(())
}
