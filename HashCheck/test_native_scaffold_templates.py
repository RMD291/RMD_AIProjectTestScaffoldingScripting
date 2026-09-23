import unittest
from pathlib import Path


class NativeScaffoldTemplateLayoutTests(unittest.TestCase):
    def test_native_template_catalog_exists_outside_cpp_source(self):
        template_root = Path(__file__).resolve().parent.parent / "NativeScaffolding" / "templates"
        self.assertTrue((template_root / "agent" / "AGENTS.md.tpl").is_file())
        self.assertTrue((template_root / "project" / "minimal" / "README.md.tpl").is_file())
        self.assertTrue((template_root / "project" / "mvc" / "README.md.tpl").is_file())


if __name__ == "__main__":
    unittest.main()
