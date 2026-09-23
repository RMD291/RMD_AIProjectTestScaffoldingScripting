# Native Scaffolding

`native_scaffold.cpp` is a platform-neutral C++17 command-line implementation of the scaffolding workflow. It uses only the C++ standard library and does not call a shell, assume a drive letter, or embed OS-specific path separators.

## Build

Use any C++17-or-newer compiler:

```text
c++ -std=c++17 -O2 -o native_scaffold native_scaffold.cpp
```

On Windows, the equivalent compiler command may produce `native_scaffold.exe`; the source and arguments remain the same.

When using WSL or another Unix-like environment, the included Makefile provides the same build plus smoke-test commands:

```text
make build
make test
make clean
```

`make test` compiles the generator and verifies MVC and agent scaffolding against the external template catalog.

## Usage

Generate a C23 project:

```text
native_scaffold ./NativeC --name "Native C App" --language c
```

Generate a C++23 project:

```text
native_scaffold ./NativeCpp --name "Native C++ App" --language cpp
```

Generate production or MVC layouts:

```text
native_scaffold ./NativeProduction --name "Native App" --language cpp --structure production
native_scaffold ./NativeMvc --name "Native App" --language cpp --structure mvc
```

Generate agent customization files:

```text
native_scaffold ./AgentProject --name "Agent Project" --kind agent
```

Existing files are skipped by default. Add `--force` to replace them explicitly.

The native implementation supports `minimal`, `production`, `website`, and `mvc` structures for C and C++. Its native directory boundaries mirror the Python generator; the Python version additionally provides C# and Java-specific build files and the external template catalog.

## Version Choices

The generated native projects target **C23** and **C++23**, the latest published stable ISO editions verified on September 22, 2026. C23 corresponds to ISO/IEC 9899:2024, and C++23 corresponds to ISO/IEC 14882:2024. The generator itself uses C++17 because that is a mature baseline supported by current compilers and is sufficient for portable filesystem and text-generation code.

## Portability

The program uses `std::filesystem::path`, binary file output, standard containers, and standard character handling. It does not use POSIX APIs, Windows APIs, shell commands, or platform-specific environment variables. The generated C/C++ programs are source-portable, but compiling them still requires a C23/C++23-capable compiler on the target operating system.