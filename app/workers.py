import os

from detection_module import hash_file


def delete_file_worker(path):
    """Deletes file from path"""
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {e}")


def hash_worker(path):
    """Return: Hashed file content"""
    try:
        h = hash_file(path)
        if h is not None:
            return (h, path)
    except Exception as e:
        print(f"Hashing error {path}: {e}")
    return None
