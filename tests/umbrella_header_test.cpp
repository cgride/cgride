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

#include <iostream>

#include <cgride/cgride.hpp>

#define CGRIDE_CHECK(expression) \
  do                             \
  {                              \
    if (!(expression))           \
    {                            \
      std::cerr                  \
          << "CHECK failed: "    \
          << #expression         \
          << '\n'                \
          << "  at "             \
          << __FILE__            \
          << ':'                 \
          << __LINE__            \
          << '\n';               \
      return 1;                  \
    }                            \
  } while (false)

int main()
{
  {
    CGRIDE_CHECK(!cgride::version_string.empty());
    CGRIDE_CHECK(cgride::api_version > 0);
  }

  {
    CGRIDE_CHECK(!cgride::core::version_string.empty());
    CGRIDE_CHECK(!cgride::project::version_string.empty());
    CGRIDE_CHECK(!cgride::graph::version_string.empty());
    CGRIDE_CHECK(!cgride::toolchains::version_string.empty());
    CGRIDE_CHECK(!cgride::executor::version_string.empty());
    CGRIDE_CHECK(!cgride::cache::version_string.empty());
    CGRIDE_CHECK(!cgride::engine::version_string.empty());
    CGRIDE_CHECK(!cgride::config::version_string.empty());
    CGRIDE_CHECK(!cgride::cli::version_string.empty());
  }

  {
    cgride::project::Project project;
    cgride::engine::BuildOptions build_options;
    cgride::config::ConfigOptions config_options;
    cgride::cli::CliOptions cli_options;

    CGRIDE_CHECK(project.targets().empty());
    CGRIDE_CHECK(build_options.valid());
    CGRIDE_CHECK(config_options.valid());
    CGRIDE_CHECK(cli_options.valid());
  }

  return 0;
}

#undef CGRIDE_CHECK
