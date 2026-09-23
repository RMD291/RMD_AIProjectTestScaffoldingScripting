import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from hash_check import CHUNK_SIZE, calculate_checksums


SCRIPT_PATH = Path(__file__).with_name("hash_check.py")


class CalculateChecksumsTests(unittest.TestCase):
    def test_calculates_all_supported_checksums(self):
        content = b"hello\n"
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "sample.txt"
            file_path.write_bytes(content)

            self.assertEqual(
                calculate_checksums(file_path),
                {
                    "MD5": "b1946ac92492d2347c6235b4d2611184",
                    "SHA-1": "f572d396fae9206628714fb2ce00f72e94f2258f",
                    "SHA-256": "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03",
                },
            )

    def test_calculates_checksums_for_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "empty.bin"
            file_path.write_bytes(b"")

            self.assertEqual(
                calculate_checksums(file_path),
                {
                    "MD5": "d41d8cd98f00b204e9800998ecf8427e",
                    "SHA-1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                    "SHA-256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                },
            )

    def test_reads_binary_data_larger_than_one_chunk(self):
        content = bytes(range(256)) * ((CHUNK_SIZE // 256) + 2)
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "binary.bin"
            file_path.write_bytes(content)

            expected = {
                "MD5": hashlib.md5(content).hexdigest(),
                "SHA-1": hashlib.sha1(content).hexdigest(),
                "SHA-256": hashlib.sha256(content).hexdigest(),
            }
            self.assertEqual(calculate_checksums(file_path), expected)


class CommandLineTests(unittest.TestCase):
    def run_script(self, file_path: Path, expected_hash: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(file_path), expected_hash],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_reports_match_case_insensitively_and_ignores_surrounding_spaces(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "sample.txt"
            file_path.write_bytes(b"hello\n")

            result = self.run_script(
                file_path,
                "  5891B5B522D5DF086D0FF0B110FBD9D21BB4FC7163AF34D08286A2E846F6BE03  ",
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("MATCH: the expected hash matches SHA-256.", result.stdout)

    def test_reports_no_match_with_non_matching_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "sample.txt"
            file_path.write_bytes(b"hello\n")

            result = self.run_script(file_path, "not-a-valid-hash")

            self.assertEqual(result.returncode, 1)
            self.assertIn("NO MATCH", result.stdout)

    def test_reports_error_for_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            missing_path = Path(directory) / "missing.bin"

            result = self.run_script(missing_path, "abc")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
