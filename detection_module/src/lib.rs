use pyo3::prelude::*;
use rayon::prelude::*;
use sha2::{Sha256, Digest};
use std::io::{BufReader, Read};
use std::fs::File;
use std::collections::HashMap;
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
    let mut map: HashMap<String, Vec<String>> = HashMap::new();

    for (hash, path) in hashes {
        map.entry(hash).or_default().push(path);
    }

    let duplicates: Vec<Vec<String>> = map
        .into_iter()
        .filter_map(|(_, paths)| if paths.len() > 1 { Some(paths) } else { None })
        .collect();

    Ok(duplicates)
}

#[pymodule]
fn detection_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_file, m)?)?;
    m.add_function(wrap_pyfunction!(find_duplicates, m)?)?;
    Ok(())
}
