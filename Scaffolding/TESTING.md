# Testing The Scaffolding Utilities

The tests use Python's built-in `unittest` module and temporary directories. They inspect generated files without requiring the .NET SDK, JDK, or Maven.

Run the Scaffolding tests from the workspace root:

```powershell
python -m unittest discover -s Scaffolding -p "test_*.py" -v
```

Run the complete repository suite:

```powershell
python -m unittest discover -s test -p "test_*.py" -v
python -m unittest discover -s Scaffolding -p "test_*.py" -v
```

## `agent_scaffold.py`

Tests verify the five-file agent customization structure, project-name substitution, preservation of existing files, explicit `--force` replacement, and the CLI report.

## `project_scaffold.py`

Tests verify:

- Portable identifiers derived from display names.
- C# project, source, and README generation.
- Java Maven project, package path, source, and README generation.
- C23 and C++23 source and README generation.
- Production layout with source, tests, documentation, and configuration areas.
- Website layout with frontend, backend, and database boundaries.
- MVC layout with models, views, controllers, tests, and configuration boundaries.
- MVC layout with models, views, controllers, tests, and configuration boundaries.
- Structure selection through the command-line interface.
- External template loading and placeholder rendering.
- Existing-file preservation.
- Invalid names and CLI language selection.

The generated projects are intentionally not compiled during unit tests. Compilation belongs to an integration check in an environment where the corresponding toolchain is installed.

## `scaffold_gui.py`

The GUI is a thin Tkinter front end over the tested `generate_project` function. Its widgets are not instantiated in headless unit tests; use `python Scaffolding/scaffold_gui.py` on a desktop with Tk available for interactive verification.

## `NativeScaffolding/native_scaffold.cpp`

Compile the native implementation with a C++17-or-newer compiler and run its CLI examples from [NativeScaffolding/README.md](../NativeScaffolding/README.md). The current environment does not provide a C++ compiler, so native compilation could not be executed here.
