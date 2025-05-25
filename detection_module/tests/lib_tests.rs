use detection_module::{hash_file, find_duplicates};
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn test_hash_file_success() {
    let mut file = NamedTempFile::new().unwrap();
    writeln!(file, "test content").unwrap();
    let path = file.path().to_str().unwrap().to_string();

    let expected_hash = "a1fff0ffefb9eace7230c24e50731f0a91c62f9cefdfe77121c2f607125dffae";
    assert_eq!(
        hash_file(path).unwrap(),
        Some(expected_hash.to_string())
    );
}

#[test]
fn test_hash_file_empty() {
    let file = NamedTempFile::new().unwrap();
    let path = file.path().to_str().unwrap().to_string();

    let expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    assert_eq!(
        hash_file(path).unwrap(),
        Some(expected_hash.to_string())
    );
}

#[test]
fn test_hash_file_nonexistent() {
    let path = "/nonexistent/path".to_string();
    assert_eq!(hash_file(path).unwrap(), None);
}

#[test]
fn test_no_duplicates() {
    let hashes = vec![
        ("hash1".to_string(), "path1".to_string()),
        ("hash2".to_string(), "path2".to_string()),
    ];

    let result = find_duplicates(hashes).unwrap();
    assert!(result.is_empty());
}

#[test]
fn test_find_duplicates_multiple_groups() {
    let hashes = vec![
        ("hash1".to_string(), "path1".to_string()),
        ("hash1".to_string(), "path2".to_string()),
        ("hash2".to_string(), "path3".to_string()),
        ("hash2".to_string(), "path4".to_string()),
    ];

    let result = find_duplicates(hashes).unwrap();
    assert_eq!(result.len(), 2);

    let mut found_group1 = false;
    let mut found_group2 = false;

    for group in result {
        if group.contains(&"path1".to_string()) {
            assert!(group.contains(&"path2".to_string()));
            assert_eq!(group.len(), 2);
            found_group1 = true;
        } else if group.contains(&"path3".to_string()) {
            assert!(group.contains(&"path4".to_string()));
            assert_eq!(group.len(), 2);
            found_group2 = true;
        }
    }

    assert!(found_group1 && found_group2);
}