<p align="center">
  <img
    src="https://res.cloudinary.com/dwjbed2xb/image/upload/v1784201609/cgride_sogdra.png"
    width="100%"
    height="650px"
    alt="Cgride banner"
  />
</p>

<p align="center">
  <strong>Build C++ with C++.</strong>
</p>

<p align="center">
  <a href="https://github.com/cgride/cgride">Repository</a>
  ·
  <a href="https://github.com/cgride/examples">Examples</a>
</p>

Cgride is an embeddable native C++ build engine with a small command-line interface on top. It is built around a simple idea: a C++ project should be describable with C++ itself, using a real API instead of a separate configuration language.

The user-facing project file is `cgride.cpp`. It defines the project, targets, sources, include directories, links, and build settings through the Cgride C++ API. The CLI reads that project description and drives the native build workflow.

```text
project/
├── cgride.cpp
└── src/
    └── main.cpp
```

A minimal project looks like this:

```cpp
#include <cgride/project.hpp>

void cgride_configure(cgride::project::Project &project)
{
  auto &app = project.executable("hello");

  app.sources("src/main.cpp");
}
```

Then the project is built and run through the CLI:

```bash
cgride build
cgride run
```

## Why Cgride exists

C++ projects already have the language, compilers, libraries, and native performance required to build serious software. The difficult part is often the layer around the compiler: project structure, targets, source discovery, include paths, dependencies, build directories, diagnostics, caching, and repeatable execution across machines.

Most build tools solve this by introducing another language or another large configuration surface. Cgride takes a different direction. It keeps the project description inside C++, so the same language used to build the application can also describe how that application is built.

This matters because build configuration is not just metadata. It is logic. Large projects often need conditions, composition, reusable functions, validation, target relationships, and integration with other developer tools. Cgride treats that as C++ code instead of turning it into a custom syntax.

## The Cgride workflow

A normal Cgride project starts with a `cgride.cpp` file at the project root. That file is the readable source of truth for the build. It declares targets and describes how they relate to the source tree.

```bash
cgride build
```

The build command loads the project description, prepares a build plan, discovers the available toolchain, builds the task graph, and executes the required work. The engine is designed to keep these steps explicit internally, so the CLI remains a thin interface over reusable C++ components.

```bash
cgride run
```

The run command builds the selected target when needed and then executes the produced binary. For projects with more than one executable, the target can be selected explicitly:

```bash
cgride build --target server
cgride run --target worker
```

The command line is intentionally small. Cgride is not meant to hide the project behind a large command surface. The core of the system is the project model, build graph, toolchain layer, executor, cache, and engine.

## C++ project descriptions

The official user project format is `cgride.cpp`.

```cpp
#include <cgride/project.hpp>

void cgride_configure(cgride::project::Project &project)
{
  auto &core = project.static_library("core");

  core.sources("core/src/message.cpp");
  core.include_dirs("core/include");

  auto &app = project.executable("app");

  app.sources("app/src/main.cpp");
  app.links(core);
}
```

This file is normal C++ code. It can use functions, constants, conditions, reusable helpers, and the type system. The intention is not to make build files clever for the sake of it, but to avoid creating a second language for decisions that C++ can express directly.

Cgride should feel natural to developers who already understand native C++ projects. Targets are targets. Sources are sources. Include directories and links are still visible. The difference is that the build description is written through a C++ API that can also be embedded by other tools.

## Embedding Cgride

The CLI is only one interface to the engine. Cgride is designed as a set of libraries that can be used directly from another C++ program.

```cpp
#include <cgride/cgride.hpp>
```

A runtime, framework, IDE integration, project generator, or higher-level developer tool can construct a Cgride project in memory, create build options, discover a toolchain, and call the build engine directly. That is the same model used behind the CLI, exposed as a public C++ API instead of being locked behind a command-line process.

This is important for tools that need native build behavior without forcing their users to manage Cgride manually. They can use Cgride as an engine and decide how much of the workflow should be visible.

## Repository structure

This repository is the umbrella repository for the Cgride modules.

```text
cgride/
├── include/
│   └── cgride/
│       ├── cgride.hpp
│       └── version.hpp
├── modules/
│   ├── core/
│   ├── project/
│   ├── graph/
│   ├── toolchains/
│   ├── executor/
│   ├── cache/
│   ├── engine/
│   ├── config/
│   └── cli/
├── examples/
├── tests/
└── cmake/
```

The umbrella target is:

```text
cgride::cgride
```

It links the public module targets together and provides the main include entry point:

```cpp
#include <cgride/cgride.hpp>
```

## Modules

Cgride is split into small modules so the build engine can remain understandable and embeddable.

`core` contains the common types used across the project: errors, results, diagnostics, paths, hashes, commands, events, cancellation, platform helpers, and version information.

`project` defines the project model. It owns concepts such as projects, targets, target kinds, source sets, requirements, visibility, build profiles, and validation.

`graph` represents the build graph. It provides tasks, task identifiers, task kinds, graph storage, and topology operations.

`toolchains` describes compiler discovery and command construction. It contains the data needed to compile, archive, and link native C++ targets.

`executor` runs build tasks and external processes. It keeps process execution, task results, and execution options separate from the higher-level build engine.

`cache` tracks file signatures, cache keys, cache entries, and cache storage. It exists so rebuild decisions can become explicit instead of being hidden inside unrelated code.

`engine` connects the project model, graph, toolchain layer, executor, and cache into the build workflow. It plans the build and returns structured results instead of exiting the process.

`config` is the loading layer. Its role is to turn a project description into a `cgride::project::Project`. The long-term user-facing format is `cgride.cpp`.

`cli` provides the user-facing command-line interface. It should remain small and call the engine instead of owning build logic itself.

## Clone

Clone the umbrella repository with its submodules:

```bash
git clone --recurse-submodules -b dev https://github.com/cgride/cgride.git
cd cgride
```

If the repository was cloned without submodules:

```bash
git submodule update --init --recursive
```

Update all submodules to their configured branches:

```bash
git submodule update --remote --recursive
```

## Build

From the umbrella repository root, configure a Ninja build directory:

```bash
cmake -S . -B build-ninja -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCGRIDE_BUILD_TESTS=ON \
  -DCGRIDE_BUILD_MODULE_TESTS=ON
```

Build everything:

```bash
cmake --build build-ninja --parallel
```

For strict local validation, use warnings as errors. In Release builds, keep assertions enabled so the test executables remain meaningful:

```bash
cmake -S . -B build-ninja -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_FLAGS="-Wall -Wextra -Wpedantic -Werror" \
  -DCMAKE_CXX_FLAGS_RELEASE="-O3" \
  -DCGRIDE_BUILD_TESTS=ON \
  -DCGRIDE_BUILD_MODULE_TESTS=ON
cmake --build build-ninja --parallel
```

Disable umbrella tests:

```bash
cmake -S . -B build-ninja -G Ninja -DCGRIDE_BUILD_TESTS=OFF
```

Disable module tests:

```bash
cmake -S . -B build-ninja -G Ninja -DCGRIDE_BUILD_MODULE_TESTS=OFF
```

## Run Tests

Run the full test suite from the generated build directory:

```bash
ctest --test-dir build-ninja --output-on-failure
```

Run only the umbrella header test:

```bash
./build-ninja/tests/cgride_umbrella_header_test
```

## Install

Install the umbrella package and all module packages from the build directory:

```bash
sudo cmake --install build-ninja --prefix /usr/local
```

The install step exports:

```text
cgride::cgride
```

It also installs the module targets required by the umbrella package, including `cgride::core`, `cgride::project`, `cgride::graph`, `cgride::toolchains`, `cgride::executor`, `cgride::cache`, `cgride::engine`, `cgride::config`, and `cgride::cli`.

After installation, another CMake project can use:

```cmake
find_package(cgride CONFIG REQUIRED)
target_link_libraries(app PRIVATE cgride::cgride)
```

and include:

```cpp
#include <cgride/cgride.hpp>
```

The install model is currently CMake-based because Cgride itself is still packaged with CMake. User projects remain Cgride projects and are built through the `cgride` CLI.

## Examples

The examples are kept in a separate submodule:

```text
examples/
├── hello/
├── static-library/
├── multiple-targets/
└── embedded-api/
```

Initialize the examples submodule:

```bash
git submodule update --init --recursive examples
```

Build and run a simple example:

```bash
cd examples/hello
cgride build
cgride run
```

The examples are intentionally small. They exist to make the public shape of Cgride clear before larger project templates are added.

See the examples repository for the current examples:

```text
https://github.com/cgride/examples
```

## Current status

Cgride is still at the foundation stage. The modules define the boundaries of the system, the umbrella package brings them together, and the examples describe the intended project shape.

The important design constraint is that the engine should remain usable as a library. Build failures, validation errors, diagnostics, and execution results should be returned as structured values. Library code should not print directly to the terminal or terminate the process. The CLI can format output for users, but the engine itself must remain embeddable.

That separation is what allows Cgride to be used both as a command-line tool and as a C++ build engine inside other software.

## Contributing

Contributions should improve the clarity, correctness, and maintainability of the build engine. Useful areas include project modeling, graph planning, toolchain discovery, execution behavior, caching, diagnostics, tests, examples, and documentation.

For larger changes, start with an issue or discussion so the design can be considered across the module boundaries.

## License

Cgride is available under the MIT License. See [LICENSE](LICENSE) for details.
