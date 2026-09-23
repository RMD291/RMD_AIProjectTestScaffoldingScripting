# File Hash Checker

`hash_check.py` calculates the MD5, SHA-1, and SHA-256 checksums of a file and compares each checksum with a hash supplied on the command line.

## Requirements

- Python 3.8 or newer
- No third-party packages

## Usage

From the workspace root, run:

```powershell
python .\test\hash_check.py <file> <expected-hash>
```

For example:

```powershell
python .\test\hash_check.py .\test\hash_check.py 6d0d4e...
```

The expected hash can use uppercase or lowercase letters and may include surrounding whitespace. The script determines which algorithm matches by comparing the supplied value with all three calculated checksums.

## Example Output

```text
File: test\hash_check.py
MD5: <calculated-md5>
SHA-1: <calculated-sha1>
SHA-256: <calculated-sha256>
MATCH: the expected hash matches SHA-256.
```

When no checksum matches, the script prints:

```text
NO MATCH: the expected hash does not match MD5, SHA-1, or SHA-256.
```

## Exit Codes

- `0`: The expected hash matches MD5, SHA-1, or SHA-256.
- `1`: The file was read successfully, but no checksum matched.
- Nonzero argparse error code: The file is missing, is not a regular file, or the command arguments are invalid.

## Security Note

MD5 and SHA-1 are included for compatibility and identification, but they are not suitable for security-sensitive integrity or authenticity checks because practical collision attacks exist. Prefer SHA-256 when the source provides it. A checksum alone does not prove who created a file; use a digital signature for authenticity.

## Tests

Run the documented test suite from the workspace root:

```powershell
python -m unittest discover -s test -p "test_*.py" -v
```

See [TESTING.md](TESTING.md) for the cases covered by the suite.
