#!/usr/bin/env python3
"""Calculate file checksums and compare them with an expected hash."""

import argparse
import hashlib
from pathlib import Path


CHUNK_SIZE = 1024 * 1024


def calculate_checksums(file_path: Path) -> dict[str, str]:
    """Calculate MD5, SHA-1, and SHA-256 checksums for a file."""
    hashers = {
        "MD5": hashlib.md5(),
        "SHA-1": hashlib.sha1(),
        "SHA-256": hashlib.sha256(),
    }

    with file_path.open("rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            for hasher in hashers.values():
                hasher.update(chunk)

    return {name: hasher.hexdigest() for name, hasher in hashers.items()}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate file checksums and compare them with an expected hash."
    )
    parser.add_argument("file", type=Path, help="Path to the file to check")
    parser.add_argument("expected_hash", help="Expected MD5, SHA-1, or SHA-256 hash")
    args = parser.parse_args()

    if not args.file.is_file():
        parser.error(f"file does not exist or is not a regular file: {args.file}")

    checksums = calculate_checksums(args.file)
    expected_hash = args.expected_hash.strip().lower()
    matches = [
        algorithm
        for algorithm, checksum in checksums.items()
        if checksum.lower() == expected_hash
    ]

    print(f"File: {args.file}")
    for algorithm, checksum in checksums.items():
        print(f"{algorithm}: {checksum}")

    if matches:
        print(f"MATCH: the expected hash matches {', '.join(matches)}.")
        return 0

    print("NO MATCH: the expected hash does not match MD5, SHA-1, or SHA-256.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
