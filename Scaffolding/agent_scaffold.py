#!/usr/bin/env python3
"""Generate a starter structure for agent customization files."""

import argparse
from pathlib import Path


TEMPLATES = {
    "AGENTS.md": """# {project_name} Agent Guidance

## Purpose

Describe the repository-wide expectations for coding agents here.

## Working Agreement

- Preserve existing conventions unless a task requires a change.
- Run the narrowest relevant test after editing.
- Explain assumptions and validation results in the final response.
""",
    ".github/agents/project.agent.md": """---
description: A focused agent for work in {project_name}
---

# Project Agent

Use this agent for changes that belong to the {project_name} repository.

## Method

1. Inspect the owning code path and nearby tests.
2. Make the smallest change that addresses the request.
3. Run a focused validation command before broad checks.
""",
    ".github/instructions/python.instructions.md": """---
applyTo: "**/*.py"
---

# Python Instructions

- Prefer the standard library when it meets the requirement.
- Keep functions small and test observable behavior.
- Use type hints for public functions.
""",
    ".github/prompts/review.prompt.md": """---
description: Review a change for correctness and regression risk
---

Review the current change in {project_name}.

Prioritize behavioral bugs, security risks, regressions, and missing tests.
Report findings first with file references, then assumptions and a concise summary.
""",
    ".github/skills/project-context/SKILL.md": """---
name: project-context
description: Explain the local conventions and validation commands for {project_name}
---

# Project Context

Use this skill when a task needs repository-specific context.

## Checklist

- Read `AGENTS.md` before making a change.
- Locate the nearest implementation and its tests.
- Use the documented project test command after editing.
""",
}


def render_templates(project_name: str) -> dict[str, str]:
    """Return the scaffold files with the project name substituted."""
    return {
        relative_path: content.format(project_name=project_name)
        for relative_path, content in TEMPLATES.items()
    }


def generate_scaffold(destination: Path, project_name: str, force: bool = False) -> tuple[list[Path], list[Path]]:
    """Create the scaffold and return (created, skipped) paths."""
    created = []
    skipped = []

    for relative_path, content in render_templates(project_name).items():
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
    parser = argparse.ArgumentParser(
        description="Generate a starter structure for agent customization files."
    )
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Directory where the structure should be created (default: current directory)",
    )
    parser.add_argument(
        "--name",
        default="Project",
        help="Project name used in generated content (default: Project)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files",
    )
    args = parser.parse_args()

    created, skipped = generate_scaffold(args.destination, args.name, args.force)
    for path in created:
        print(f"CREATED: {path}")
    for path in skipped:
        print(f"SKIPPED: {path}")
    print(f"Generated {len(created)} file(s); skipped {len(skipped)} existing file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())