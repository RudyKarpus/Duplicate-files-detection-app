use pyo3::prelude::*;
use rayon::prelude::*;
use sha2::{Sha256, Digest};
use std::io::{BufReader, Read};
use std::fs::File;

#[pyfunction]
fn hash_file(path: String) -> PyResult<Option<String>> {
    let file = match File::open(&path) {
        Ok(f) => f,
        Err(_) => return Ok(None),
    };
    let mut reader = BufReader::new(file);
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024];

    loop {
        let count = reader.read(&mut buffer)?;
        if count == 0 {
            break;
        }
        hasher.update(&buffer[..count]);
    }

    Ok(Some(format!("{:x}", hasher.finalize())))
}
#[pyfunction]
fn find_duplicates(hashes: Vec<(String, String)>) -> PyResult<Vec<Vec<String>>> {
    let m = (0..2)
        .map(|i| (0..2).map(|j| format!("({},{})", i, j)).collect())
        .collect();
    Ok(m)
}

#[pymodule]
fn detection_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_file, m)?)?;
    m.add_function(wrap_pyfunction!(find_duplicates, m)?)?;
    Ok(())
}
