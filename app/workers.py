import os

from detection_module import hash_file


def delete_file_worker(path):
    """Deletes file from path"""

    if not os.path.isfile(path=path):
        print(f"There is no such a file {path}")
        return None

    try:
        os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {e}")


def hash_worker(path):
    """Return: Hashed file content and path"""

    if not os.path.isfile(path=path):
        print(f"There is no such a file {path}")
        return None

    try:
        h = hash_file(path)
        if h is not None:
            return (h, path)
    except Exception as e:
        print(f"Hashing error {path}: {e}")
    return None
