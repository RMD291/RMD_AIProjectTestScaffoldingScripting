# Testing `hash_check.py`

The test suite uses Python's built-in `unittest` module and requires no third-party packages.

From the workspace root (`d:\Projects\AI`), run:

```powershell
python -m unittest discover -s test -p "test_*.py" -v
```

## Covered cases

- Correct MD5, SHA-1, and SHA-256 values for a known text file.
- Correct well-known checksums for an empty file.
- Binary data larger than the one-megabyte read buffer, exercising multiple read chunks.
- A matching hash using uppercase letters and surrounding whitespace.
- A non-matching hash, including the expected nonzero exit status.
- A missing input file and the resulting command-line error.

The command-line tests execute `hash_check.py` in a separate Python process, which verifies the printed messages and exit codes rather than only testing the internal function.

