import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from project_scaffold import (
    C_STANDARD,
    CPP_STANDARD,
    DOTNET_TARGET_FRAMEWORK,
    JAVA_RELEASE,
    generate_project,
    project_identifier,
    render_templates,
)


SCRIPT_PATH = Path(__file__).with_name("project_scaffold.py")


class ProjectScaffoldTests(unittest.TestCase):
    def test_normalizes_display_name_for_project_identifiers(self):
        self.assertEqual(project_identifier("weather dashboard"), "WeatherDashboard")
        self.assertEqual(project_identifier("2026 notes"), "App2026Notes")

    def test_generates_csharp_console_project(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(destination, "Weather App", "csharp")

            self.assertEqual(len(created), 3)
            self.assertEqual(skipped, [])
            self.assertTrue((destination / "WeatherApp.csproj").is_file())
            project_file = (destination / "WeatherApp.csproj").read_text(encoding="utf-8")
            self.assertIn(f"<TargetFramework>{DOTNET_TARGET_FRAMEWORK}</TargetFramework>", project_file)
            program = (destination / "Program.cs").read_text(encoding="utf-8")
            self.assertIn("namespace WeatherApp;", program)
            self.assertIn("Hello from Weather App!", program)

    def test_generates_java_maven_project(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(destination, "Weather App", "java")

            self.assertEqual(len(created), 3)
            self.assertEqual(skipped, [])
            source = destination.joinpath(
                "src", "main", "java", "com", "example", "weatherapp", "App.java"
            )
            self.assertTrue(source.is_file())
            self.assertIn("package com.example.weatherapp;", source.read_text(encoding="utf-8"))
            pom = (destination / "pom.xml").read_text(encoding="utf-8")
            self.assertIn("<artifactId>weatherapp</artifactId>", pom)
            self.assertIn(f"<maven.compiler.release>{JAVA_RELEASE}</maven.compiler.release>", pom)

    def test_skips_existing_files_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            target = destination / "Program.cs"
            target.write_text("custom program\n", encoding="utf-8")

            created, skipped = generate_project(destination, "Sample", "csharp")

            self.assertEqual(len(created), 2)
            self.assertEqual(skipped, [target])
            self.assertEqual(target.read_text(encoding="utf-8"), "custom program\n")

    def test_rejects_empty_project_name(self):
        with self.assertRaises(ValueError):
            render_templates("---", "java")

    def test_generates_c23_project(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(destination, "Native App", "c")

            self.assertEqual(len(created), 2)
            self.assertEqual(skipped, [])
            self.assertIn("#include <stdio.h>", (destination / "main.c").read_text(encoding="utf-8"))
            self.assertIn(C_STANDARD, (destination / "README.md").read_text(encoding="utf-8"))

    def test_generates_cpp23_project(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(destination, "Native App", "cpp")

            self.assertEqual(len(created), 2)
            self.assertEqual(skipped, [])
            self.assertIn("#include <iostream>", (destination / "main.cpp").read_text(encoding="utf-8"))
            self.assertIn(CPP_STANDARD, (destination / "README.md").read_text(encoding="utf-8"))

    def test_generates_production_csharp_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(
                destination, "Orders App", "csharp", structure="production"
            )

            self.assertEqual(len(created), 7)
            self.assertEqual(skipped, [])
            self.assertTrue((destination / "src/OrdersApp/OrdersApp.csproj").is_file())
            self.assertTrue((destination / "src/OrdersApp/Program.cs").is_file())
            self.assertTrue((destination / "tests/README.md").is_file())
            self.assertTrue((destination / "docs/README.md").is_file())
            self.assertTrue((destination / "config/README.md").is_file())

    def test_generates_website_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(
                destination, "Storefront", "cpp", structure="website"
            )

            self.assertEqual(len(created), 8)
            self.assertEqual(skipped, [])
            for relative_path in (
                "frontend/README.md",
                "frontend/src/.gitkeep",
                "backend/README.md",
                "backend/src/.gitkeep",
                "database/README.md",
                "database/migrations/.gitkeep",
                ".gitignore",
            ):
                self.assertTrue((destination / relative_path).is_file())

    def test_generates_mvc_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(
                destination, "Inventory", "csharp", structure="mvc"
            )

            self.assertEqual(len(created), 10)
            self.assertEqual(skipped, [])
            for relative_path in (
                "models/README.md",
                "models/.gitkeep",
                "views/README.md",
                "views/.gitkeep",
                "controllers/README.md",
                "controllers/.gitkeep",
                "tests/README.md",
                "config/README.md",
                ".gitignore",
            ):
                self.assertTrue((destination / relative_path).is_file())
            self.assertIn(
                "Model-View-Controller",
                (destination / "README.md").read_text(encoding="utf-8"),
            )

    def test_generates_mvc_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            created, skipped = generate_project(
                destination, "Inventory", "csharp", structure="mvc"
            )

            self.assertEqual(len(created), 10)
            self.assertEqual(skipped, [])
            for relative_path in (
                "models/README.md",
                "models/.gitkeep",
                "views/README.md",
                "views/.gitkeep",
                "controllers/README.md",
                "controllers/.gitkeep",
                "tests/README.md",
                "config/README.md",
                ".gitignore",
            ):
                self.assertTrue((destination / relative_path).is_file())
            self.assertIn(
                "Model-View-Controller",
                (destination / "README.md").read_text(encoding="utf-8"),
            )

    def test_rejects_unknown_structure(self):
        with self.assertRaises(ValueError):
            render_templates("Sample", "csharp", structure="mobile")


class CommandLineTests(unittest.TestCase):
    def test_generates_selected_language_from_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    directory,
                    "--name",
                    "CLI App",
                    "--language",
                    "java",
                    "--structure",
                    "production",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Generated 7 file(s)", result.stdout)
            self.assertTrue((Path(directory) / "pom.xml").is_file())


if __name__ == "__main__":
    unittest.main()