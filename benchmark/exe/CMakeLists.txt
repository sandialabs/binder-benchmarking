set(TARGET cpp_speedtest)

add_executable(${TARGET} benchmark.cpp)

target_link_libraries(${TARGET}
  PRIVATE
    ${CMAKE_PROJECT_NAME}::mechanization
    ${CMAKE_PROJECT_NAME}::geodetic
    ${CMAKE_PROJECT_NAME}::test_common
)
