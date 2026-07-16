add_executable(cgride_umbrella_header_test
  umbrella_header_test.cpp
)

target_link_libraries(cgride_umbrella_header_test
  PRIVATE
    cgride::cgride
)

target_compile_features(cgride_umbrella_header_test
  PRIVATE
    cxx_std_23
)

set_target_properties(cgride_umbrella_header_test
  PROPERTIES
    CXX_EXTENSIONS OFF
)

add_test(
  NAME cgride_umbrella_header_test
  COMMAND cgride_umbrella_header_test
)


find_package(Python3 COMPONENTS Interpreter QUIET)

if(Python3_Interpreter_FOUND)
  add_test(
    NAME cgride_cli_noop_integration_test
    COMMAND
      ${Python3_EXECUTABLE}
      ${CMAKE_CURRENT_SOURCE_DIR}/cli_noop_integration_test.py
      $<TARGET_FILE:cgride_cli_bin>
      ${PROJECT_BINARY_DIR}
  )
endif()
