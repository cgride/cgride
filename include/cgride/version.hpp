/**
 *
 *  @file version.hpp
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
#ifndef CGRIDE_VERSION_HPP
#define CGRIDE_VERSION_HPP

#include <string_view>

namespace cgride
{
  /**
   * @brief Major version of Cgride.
   */
  inline constexpr int version_major = 0;

  /**
   * @brief Minor version of Cgride.
   */
  inline constexpr int version_minor = 1;

  /**
   * @brief Patch version of Cgride.
   */
  inline constexpr int version_patch = 0;

  /**
   * @brief Public API version of Cgride.
   */
  inline constexpr int api_version = 1;

  /**
   * @brief Human-readable version string.
   */
  inline constexpr std::string_view version_string = "0.1.0";

} // namespace cgride

#endif // CGRIDE_VERSION_HPP
