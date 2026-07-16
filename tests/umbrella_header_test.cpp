/**
 *
 *  @file umbrella_header_test.cpp
 *  @author Gaspard Kirira
 *
 *  Copyright 2026, Gaspard Kirira.
 *  All rights reserved.
 *  https://github.com/cgride/cgride
 *
 *  Use of this source code is governed by an MIT license
 *  that can be found in the LICENSE file.
 *
 *  Cgride
 *
 */
#include <cassert>
#include <string_view>

#include <cgride/cgride.hpp>

int main()
{
  {
    assert(cgride::version_major == 0);
    assert(cgride::version_minor == 1);
    assert(cgride::version_patch == 0);
    assert(cgride::api_version == 1);
    assert(cgride::version_string == std::string_view("0.1.0"));
  }

  {
    assert(cgride::core::version_string == std::string_view("0.1.0"));
    assert(cgride::project::version_string == std::string_view("0.1.0"));
    assert(cgride::graph::version_string == std::string_view("0.1.0"));
    assert(cgride::toolchains::version_string == std::string_view("0.1.0"));
    assert(cgride::executor::version_string == std::string_view("0.1.0"));
    assert(cgride::cache::version_string == std::string_view("0.1.0"));
    assert(cgride::engine::version_string == std::string_view("0.1.0"));
    assert(cgride::config::version_string == std::string_view("0.1.0"));
    assert(cgride::cli::version_string == std::string_view("0.1.0"));
  }

  {
    cgride::project::Project project;
    cgride::engine::BuildOptions build_options;
    cgride::config::ConfigOptions config_options;
    cgride::cli::CliOptions cli_options;

    assert(project.targets().empty());
    assert(build_options.valid());
    assert(config_options.valid());
    assert(cli_options.valid());
  }

  return 0;
}
