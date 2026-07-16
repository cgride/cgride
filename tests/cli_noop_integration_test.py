#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def run(command, cwd, env):
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require(condition, message, process=None):
    if condition:
        return

    print(message, file=sys.stderr)

    if process is not None:
        print("stdout:", process.stdout, file=sys.stderr)
        print("stderr:", process.stderr, file=sys.stderr)
        print("returncode:", process.returncode, file=sys.stderr)

    raise SystemExit(1)


def install_package(build_dir, prefix):
    install = subprocess.run(
        ["cmake", "--install", str(build_dir), "--prefix", str(prefix)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(install.returncode == 0, "installing cgride package for integration test failed", install)


def write_project(root, message):
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "cgride.cpp").write_text(
        '#include <cgride/project.hpp>\n\n'
        'void cgride_configure(cgride::project::Project &project)\n'
        '{\n'
        '  auto &app = project.executable("hello");\n'
        '  app.sources("src/main.cpp");\n'
        '}\n'
    )
    (root / "src" / "main.cpp").write_text(
        '#include <iostream>\n\n'
        'int main()\n'
        '{\n'
        f'  std::cout << "{message}\\n";\n'
        '}\n'
    )


def main():
    if len(sys.argv) != 3:
        print("usage: cli_noop_integration_test.py <cgride> <build-dir>", file=sys.stderr)
        return 2

    cgride = Path(sys.argv[1]).resolve()
    build_dir = Path(sys.argv[2]).resolve()

    require(cgride.exists(), f"cgride executable does not exist: {cgride}")
    require(build_dir.exists(), f"build directory does not exist: {build_dir}")

    workspace = Path(tempfile.mkdtemp(prefix="cgride-noop-"))

    try:
        install_prefix = workspace / "prefix"
        install_package(build_dir, install_prefix)

        env = os.environ.copy()
        env["CGRIDE_PREFIX_PATH"] = str(install_prefix)

        write_project(workspace, "hello from noop test")

        first = run([str(cgride), "build"], workspace, env)
        require(first.returncode == 0, "first build failed", first)

        helper = workspace / ".cgride" / "config" / "build" / "bin" / ("cgride_config.exe" if os.name == "nt" else "cgride_config")
        require(helper.exists(), "config helper was not produced")
        helper_mtime = helper.stat().st_mtime_ns

        second = run([str(cgride), "build", "-v"], workspace, env)
        require(second.returncode == 0, "second build failed", second)
        require("config: fresh" in second.stdout, "second build did not use fresh config helper", second)
        require("cgride fresh hello" in second.stdout, "second build was not reported as fresh", second)
        require(helper.stat().st_mtime_ns == helper_mtime, "second build recompiled cgride.cpp helper")

        first_run = run([str(cgride), "run"], workspace, env)
        require(first_run.returncode == 0, "run failed", first_run)
        require(first_run.stdout == "hello from noop test\n", "run output was not clean program output", first_run)

        time.sleep(0.02)
        (workspace / "src" / "main.cpp").write_text(
            '#include <iostream>\n\n'
            'int main()\n'
            '{\n'
            '  std::cout << "hello after source touch\\n";\n'
            '}\n'
        )

        source_rebuild = run([str(cgride), "build"], workspace, env)
        require(source_rebuild.returncode == 0, "source rebuild failed", source_rebuild)
        require("cgride built hello" in source_rebuild.stdout, "touching source did not rebuild target", source_rebuild)

        helper_mtime = helper.stat().st_mtime_ns
        time.sleep(0.02)
        (workspace / "cgride.cpp").write_text(
            '#include <cgride/project.hpp>\n\n'
            'void cgride_configure(cgride::project::Project &project)\n'
            '{\n'
            '  auto &app = project.executable("hello");\n'
            '  app.sources("src/main.cpp");\n'
            '  app.compile_definition("CGRIDE_NOOP_TEST");\n'
            '}\n'
        )

        config_rebuild = run([str(cgride), "build", "-v"], workspace, env)
        require(config_rebuild.returncode == 0, "config rebuild failed", config_rebuild)
        require("config: rebuilding" in config_rebuild.stdout, "touching cgride.cpp did not rebuild config helper", config_rebuild)
        require(helper.stat().st_mtime_ns != helper_mtime, "config helper timestamp did not change after cgride.cpp change")

    finally:
        shutil.rmtree(workspace, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
