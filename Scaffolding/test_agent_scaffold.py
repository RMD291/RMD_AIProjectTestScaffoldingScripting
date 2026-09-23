import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_scaffold import TEMPLATES, generate_scaffold


SCRIPT_PATH = Path(__file__).with_name("agent_scaffold.py")


class GenerateScaffoldTests(unittest.TestCase):
    def test_creates_expected_structure_and_substitutes_name(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_scaffold(destination, "Widget Lab")

            self.assertEqual(len(created), len(TEMPLATES))
            self.assertEqual(skipped, [])
            for relative_path in TEMPLATES:
                file_path = destination / relative_path
                self.assertTrue(file_path.is_file())
                if "{project_name}" in TEMPLATES[relative_path]:
                    self.assertIn("Widget Lab", file_path.read_text(encoding="utf-8"))

    def test_skips_existing_files_without_overwriting_them(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            target = destination / "AGENTS.md"
            target.write_text("custom guidance\n", encoding="utf-8")

            created, skipped = generate_scaffold(destination, "Widget Lab")

            self.assertEqual(len(created), len(TEMPLATES) - 1)
            self.assertIn(target, skipped)
            self.assertEqual(target.read_text(encoding="utf-8"), "custom guidance\n")

    def test_force_replaces_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            target = destination / "AGENTS.md"
            target.write_text("custom guidance\n", encoding="utf-8")

            created, skipped = generate_scaffold(destination, "Widget Lab", force=True)

            self.assertEqual(len(created), len(TEMPLATES))
            self.assertEqual(skipped, [])
            self.assertIn("Widget Lab", target.read_text(encoding="utf-8"))


class CommandLineTests(unittest.TestCase):
    def test_reports_created_files(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), directory, "--name", "CLI Lab"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Generated 5 file(s)", result.stdout)
            self.assertTrue((Path(directory) / ".github/agents/project.agent.md").is_file())


if __name__ == "__main__":
    unittest.main()