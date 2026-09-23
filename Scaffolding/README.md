# Scaffolding Utilities

This folder contains two independent Python scripts for creating repeatable starter files. Both use only the standard library and protect existing files unless `--force` is supplied.

## Agent Customization Scaffold

`agent_scaffold.py` creates coding-agent customization files:

```text
AGENTS.md
.github/
  agents/project.agent.md
  instructions/python.instructions.md
  prompts/review.prompt.md
  skills/project-context/SKILL.md
```

Run it from the workspace root:

```powershell
python .\Scaffolding\agent_scaffold.py . --name "My Project"
```

## Application Project Scaffold

`project_scaffold.py` creates a minimal console application in C#, Java, C, or C++:

```powershell
python .\Scaffolding\project_scaffold.py .\WeatherApp --name "Weather App" --language csharp
python .\Scaffolding\project_scaffold.py .\WeatherAppJava --name "Weather App" --language java
python .\Scaffolding\project_scaffold.py .\NativeC --name "Native C App" --language c
python .\Scaffolding\project_scaffold.py .\NativeCpp --name "Native C++ App" --language cpp
python .\Scaffolding\project_scaffold.py .\OrdersApp --name "Orders App" --language csharp --structure production
python .\Scaffolding\project_scaffold.py .\Storefront --name "Storefront" --language java --structure website
python .\Scaffolding\project_scaffold.py .\Inventory --name "Inventory" --language csharp --structure mvc
```

The C# output contains a .NET 10 SDK-style project, `Program.cs`, and a README. The Java output contains a Maven `pom.xml`, a package-correct `App.java`, and a README for a Java 25 application. The native outputs contain `main.c` or `main.cpp` and target C23 or C++23.

### Structure Profiles

Use `--structure` to choose the intended level of organization:

- `minimal` (default): the smallest runnable starter files.
- `production`: root README, `src/`, `tests/`, `docs/`, `config/`, and language-specific source placement.
- `website`: separate `frontend/`, `backend/`, and `database/` boundaries, starter READMEs, placeholders, and a shared `.gitignore`.
- `mvc`: separate `models/`, `views/`, `controllers/`, `tests/`, and `config/` areas.

The website profile is intentionally technology-neutral. It creates boundaries without assuming a frontend framework, backend framework, database engine, or deployment provider.

## Template Files And GUI

Template content is stored under [`templates/`](templates/) as readable UTF-8 `.tpl` files. Python contains the profile manifest, placeholder values, and file-writing logic; template prose and starter source remain editable without changing the generator.

Launch the optional standard-library Tkinter interface from the workspace root:

```powershell
python .\Scaffolding\scaffold_gui.py
```

The GUI selects the same destination, name, language, structure, and overwrite options as the CLI. It delegates to `generate_project`, so both interfaces produce identical files.

## Native C++ Implementation

The separate [NativeScaffolding](../NativeScaffolding/README.md) folder contains `native_scaffold.cpp`, a C++17 implementation of the agent and native project workflows. It uses standard-library filesystem and file APIs, accepts the same skip/force model, and does not depend on Windows, POSIX, or a shell.

## Process And Choices

The application scaffold follows this pipeline:

1. Parse the destination, display name, language, and optional overwrite flag.
2. Normalize the display name into a portable identifier for namespaces, packages, and filenames.
3. Select and render the language-specific templates.
4. Create parent directories and write files, skipping existing files unless replacement is explicit.
5. Report created and skipped paths.

Templates remain in the script so output is deterministic, easy to audit, and dependency-free. C# uses the compact SDK-style format because it is the standard modern console-project shape. Java uses Maven because `pom.xml` provides a conventional build entry point and dependency boundary. The generator does not run .NET, Java, or Maven commands; those are runtime prerequisites for projects it creates.

The existing project scaffold was updated instead of creating a second script. This keeps one documented command and one tested implementation for each supported language. The version values are named constants so the next LTS transition has a single clear update point.

## Requirements

- Python 3.9 or newer
- No third-party Python packages
- .NET 10 SDK to run generated C# projects
- JDK 25 and Maven to build generated Java projects

See [TESTING.md](TESTING.md) for the test commands and covered behavior.
