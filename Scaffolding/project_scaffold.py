#!/usr/bin/env python3
"""Generate project structures from external templates."""

import argparse
import re
from pathlib import Path

SUPPORTED_LANGUAGES = ("csharp", "java", "c", "cpp")
SUPPORTED_STRUCTURES = ("minimal", "production", "website", "mvc")
DOTNET_TARGET_FRAMEWORK = "net10.0"

JAVA_RELEASE = "25"
C_STANDARD = "c23"
CPP_STANDARD = "c++23"

TEMPLATE_ROOT = Path(__file__).with_name("templates")


def project_identifier(project_name: str) -> str:
    """Convert a display name into a valid, portable project identifier."""
    words = re.findall(r"[A-Za-z0-9]+", project_name)
    identifier = "".join(word[:1].upper() + word[1:] for word in words)
    if not identifier:
        raise ValueError("project name must contain at least one letter or digit")
    if identifier[0].isdigit():
        identifier = f"App{identifier}"
    return identifier

def _render(template_name: str, values: dict[str, str]) -> str:
    """Read and render one external UTF-8 template."""
    template_path = TEMPLATE_ROOT / template_name

    try:
        template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise RuntimeError(f"template is missing: {template_path}") from error
    return template.format(**values)


def _values(project_name: str) -> dict[str, str]:
    identifier = project_identifier(project_name)
    return {
        "project_name": project_name,
        "identifier": identifier,
        "package_name": identifier.lower(),
        "dotnet_target_framework": DOTNET_TARGET_FRAMEWORK,
        "java_release": JAVA_RELEASE,
    }

def render_templates(
    project_name: str,
    language: str,
    structure: str = "minimal",
) -> dict[str, str]:
    """Return rendered project files for a language and structure profile."""
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"unsupported language: {language}")
    if structure not in SUPPORTED_STRUCTURES:
        raise ValueError(f"unsupported structure: {structure}")

    values = _values(project_name)
    if structure == "minimal":
        if language == "csharp":
            files = {
                "{identifier}.csproj": "minimal/csharp/project.csproj.tpl",
                "Program.cs": "minimal/csharp/Program.cs.tpl",
                "README.md": "minimal/csharp/README.md.tpl",
            }
        elif language == "java":
            files = {
                "pom.xml": "minimal/java/pom.xml.tpl",
                "src/main/java/com/example/{package_name}/App.java": "minimal/java/App.java.tpl",
                "README.md": "minimal/java/README.md.tpl",
            }
        else:
            extension = "c" if language == "c" else "cpp"
            values["native_language"] = "C" if language == "c" else "C++"
            values["native_standard"] = C_STANDARD if language == "c" else CPP_STANDARD
            files = {
                f"main.{extension}": f"minimal/{language}/main.{extension}.tpl",
                "README.md": "minimal/native-readme.md.tpl",
            }
    elif structure == "production":
        files = {
            "README.md": "shared/production/README.md.tpl",
            "tests/README.md": "shared/production/tests-README.md.tpl",
            "docs/README.md": "shared/production/docs-README.md.tpl",
            "config/README.md": "shared/production/config-README.md.tpl",
            ".gitignore": "shared/production/gitignore.tpl",
        }

        if language == "csharp":
            files.update(
                {
                    "src/{identifier}/{identifier}.csproj": "minimal/csharp/project.csproj.tpl",
                    "src/{identifier}/Program.cs": "minimal/csharp/Program.cs.tpl",
                }
            )
        elif language == "java":
            files.update(
                {
                    "pom.xml": "minimal/java/pom.xml.tpl",
                    "src/main/java/com/example/{package_name}/App.java": "minimal/java/App.java.tpl",
                }
            )
        else:
            extension = "c" if language == "c" else "cpp"
            files[f"src/main.{extension}"] = f"minimal/{language}/main.{extension}.tpl"
    elif structure == "website":
        files = {
            "README.md": "shared/website/README.md.tpl",
            "frontend/README.md": "shared/website/frontend-README.md.tpl",
            "frontend/src/.gitkeep": None,
            "backend/README.md": "shared/website/backend-README.md.tpl",
            "backend/src/.gitkeep": None,
            "database/README.md": "shared/website/database-README.md.tpl",
            "database/migrations/.gitkeep": None,
            ".gitignore": "shared/website/gitignore.tpl",
        }
    else:
        files = {
            "README.md": "shared/mvc/README.md.tpl",
            "models/README.md": "shared/mvc/models-README.md.tpl",
            "models/.gitkeep": None,
            "views/README.md": "shared/mvc/views-README.md.tpl",
            "views/.gitkeep": None,
            "controllers/README.md": "shared/mvc/controllers-README.md.tpl",
            "controllers/.gitkeep": None,
            "tests/README.md": "shared/mvc/tests-README.md.tpl",
            "config/README.md": "shared/mvc/config-README.md.tpl",
            ".gitignore": "shared/mvc/gitignore.tpl",
        }

    rendered = {}
    for output_path, template_name in files.items():
        rendered_path = output_path.format(**values)
        rendered[rendered_path] = "" if template_name is None else _render(template_name, values)

    return rendered

def generate_project(
    destination: Path,
    project_name: str,

    language: str,
    force: bool = False,
    structure: str = "minimal",
) -> tuple[list[Path], list[Path]]:
    """Create project files and return (created, skipped) paths."""
    created = []
    skipped = []
    templates = render_templates(project_name, language, structure)
    for relative_path, content in templates.items():
        file_path = destination / relative_path
        if file_path.exists() and not force:
            skipped.append(file_path)
            continue
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8", newline="\n") as file:
            file.write(content)
        created.append(file_path)
    return created, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a project from external templates.")
    parser.add_argument("destination", type=Path, help="Directory for the generated project")
    parser.add_argument("--name", required=True, help="Display name for the application")
    parser.add_argument("--language", required=True, choices=SUPPORTED_LANGUAGES)
    parser.add_argument("--structure", choices=SUPPORTED_STRUCTURES, default="minimal")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()
    try:
        created, skipped = generate_project(
            args.destination, args.name, args.language, args.force, args.structure
        )
    except (RuntimeError, ValueError) as error:
        parser.error(str(error))

    for path in created:
        print(f"CREATED: {path}")
    for path in skipped:
        print(f"SKIPPED: {path}")
    print(f"Generated {len(created)} file(s); skipped {len(skipped)} existing file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
