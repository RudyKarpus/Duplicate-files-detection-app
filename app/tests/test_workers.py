import hashlib
import os
import tempfile
import unittest
from unittest.mock import patch

from app.workers import delete_file_worker, hash_worker


def create_temp_file(content=None):
    """Helper to create temporary file with optional content"""
    fd, path = tempfile.mkstemp()
    if content:
        os.write(fd, content.encode())
    os.close(fd)
    return path


class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.empty_file = create_temp_file()
        self.content_file = create_temp_file("test content")
        self.nonexistent_file = "/path/that/does/not/exist.txt"

    def tearDown(self):
        for path in [self.empty_file, self.content_file]:
            if os.path.exists(path):
                os.remove(path)

    # Tests for delete_file_worker
    def test_delete_file_success(self):
        """Test successful file deletion"""
        self.assertTrue(os.path.exists(self.empty_file))
        delete_file_worker(self.empty_file)
        self.assertFalse(os.path.exists(self.empty_file))

    def test_delete_nonexistent_file(self):
        """Test deleting non-existent file (should fail silently)"""
        with patch("builtins.print") as mock_print:
            delete_file_worker(self.nonexistent_file)
            mock_print.assert_called_once()
            self.assertIn("There is no such a file", mock_print.call_args[0][0])

    def test_delete_file_permission_error(self):
        """Test deletion with permission error"""
        if os.name == "nt":
            self.skipTest("Permission test not reliable on Windows")

        protected_file = create_temp_file()
        # read only
        os.chmod(protected_file, 0o400)

        with patch("builtins.print") as mock_print:
            delete_file_worker(protected_file)
            mock_print.assert_called_once()
            self.assertIn("Error deleting file", mock_print.call_args[0][0])

        os.chmod(protected_file, 0o700)
        os.remove(protected_file)

    # Tests for hash_worker
    def test_hash_file_success(self):
        """Test successful file hashing"""
        expected_hash = hashlib.sha256(b"test content").hexdigest()
        result = hash_worker(self.content_file)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], expected_hash)
        self.assertEqual(result[1], self.content_file)

    def test_hash_empty_file(self):
        """Test hashing empty file"""
        expected_hash = hashlib.sha256(b"").hexdigest()
        result = hash_worker(self.empty_file)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], expected_hash)

    def test_hash_nonexistent_file(self):
        """Test hashing non-existent file"""
        with patch("builtins.print") as mock_print:
            result = hash_worker(self.nonexistent_file)
            self.assertIsNone(result)
            mock_print.assert_called_once()
            self.assertIn("There is no such a file", mock_print.call_args[0][0])

    def test_hash_unreadable_file(self):
        """Test hashing unreadable file"""
        if os.name == "nt":
            self.skipTest("Permission test not reliable on Windows")

        protected_file = create_temp_file("can't read me")
        # no permision
        os.chmod(protected_file, 0o000)

        with patch("builtins.print") as mock_print:
            result = hash_worker(protected_file)
            self.assertIsNone(result)
            mock_print.assert_called_once()
            self.assertIn("Hashing error", mock_print.call_args[0][0])

        os.chmod(protected_file, 0o700)
        os.remove(protected_file)


if __name__ == "__main__":
    unittest.main()
