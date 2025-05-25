import os
import tempfile
import unittest

from app.utils import scan_folder


class TestFolderScanning(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.temp_dir, "subfolder")
        os.mkdir(self.sub_dir)

        self.file1 = os.path.join(self.temp_dir, "file1.txt")
        self.file2 = os.path.join(self.temp_dir, "file2.log")
        self.file3 = os.path.join(self.sub_dir, "file3.dat")

        for file_path in [self.file1, self.file2, self.file3]:
            with open(file_path, "w") as f:
                f.write("test content")

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_scan_folder(self):
        """Test scanning folder with multiple files"""
        result = scan_folder(self.temp_dir)
        self.assertEqual(len(result), 3)
        self.assertIn(self.file1, result)
        self.assertIn(self.file2, result)
        self.assertIn(self.file3, result)

    def test_scan_empty_folder(self):
        """Test scanning empty folder"""
        empty_dir = os.path.join(self.temp_dir, "empty")
        os.mkdir(empty_dir)
        result = scan_folder(empty_dir)
        self.assertEqual(result, [])

    def test_scan_nonexistent_folder(self):
        """Test scanning non-existent folder"""
        non_existent = os.path.join(self.temp_dir, "does_not_exist")
        result = scan_folder(non_existent)
        self.assertEqual(result, [])

    def test_scan_file_instead_of_folder(self):
        """Test passing a file path instead of folder"""
        result = scan_folder(self.file1)
        self.assertEqual(result, [])

    def test_scan_folder_permission_denied(self):
        """Test scanning folder with permission restrictions"""
        if os.name == "nt":
            self.skipTest("Permission tests not reliable on Windows")

        restricted_dir = os.path.join(self.temp_dir, "restricted")
        # No permission
        os.mkdir(restricted_dir, 0o000)

        with self.assertRaises(PermissionError):
            scan_folder(restricted_dir)

        os.chmod(restricted_dir, 0o700)
        os.rmdir(restricted_dir)


if __name__ == "__main__":
    unittest.main()
