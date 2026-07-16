cmake_minimum_required(VERSION 3.22)

project(
  cgride
  VERSION 0.1.0
  DESCRIPTION "Embeddable native C++ build engine with a minimal CLI."
  HOMEPAGE_URL "https://github.com/cgride/cgride"
  LANGUAGES CXX
)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

option(CGRIDE_BUILD_TESTS "Build Cgride umbrella tests" ON)
option(CGRIDE_BUILD_MODULE_TESTS "Build tests for Cgride modules" ON)
option(CGRIDE_INSTALL "Install Cgride umbrella package" ON)

if(NOT CGRIDE_BUILD_MODULE_TESTS)
  set(CGRIDE_CORE_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_PROJECT_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_GRAPH_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_TOOLCHAINS_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_EXECUTOR_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_CACHE_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_ENGINE_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_CONFIG_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CGRIDE_CLI_BUILD_TESTS OFF CACHE BOOL "" FORCE)
endif()

add_subdirectory(modules/core)
add_subdirectory(modules/project)
add_subdirectory(modules/graph)
add_subdirectory(modules/toolchains)
add_subdirectory(modules/executor)
add_subdirectory(modules/cache)
add_subdirectory(modules/engine)
add_subdirectory(modules/config)
add_subdirectory(modules/cli)

add_library(cgride INTERFACE)
add_library(cgride::cgride ALIAS cgride)

target_compile_features(cgride
  INTERFACE
    cxx_std_23
)

target_include_directories(cgride
  INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_link_libraries(cgride
  INTERFACE
    cgride::core
    cgride::project
    cgride::graph
    cgride::toolchains
    cgride::executor
    cgride::cache
    cgride::engine
    cgride::config
    cgride::cli
)

set_target_properties(cgride
  PROPERTIES
    EXPORT_NAME cgride
)

if(CGRIDE_BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()

if(CGRIDE_INSTALL)
  install(
    TARGETS cgride
    EXPORT cgride-targets
  )

  install(
    DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  )

  install(
    EXPORT cgride-targets
    NAMESPACE cgride::
    FILE cgride-targets.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/cgride
  )

  configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/cgride-config.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cgride-config.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/cgride
  )

  write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/cgride-config-version.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
  )

  install(
    FILES
      ${CMAKE_CURRENT_BINARY_DIR}/cgride-config.cmake
      ${CMAKE_CURRENT_BINARY_DIR}/cgride-config-version.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/cgride
  )
endif()
