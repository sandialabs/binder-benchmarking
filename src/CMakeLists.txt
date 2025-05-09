# Units library
set(TARGET batch_call)

add_library(${TARGET} INTERFACE)
add_library(${CMAKE_PROJECT_NAME}::${TARGET} ALIAS ${TARGET})


# Set a few things for any future targets linking to this target
# Ensure access to headers
target_include_directories(${TARGET} INTERFACE ./)

target_link_libraries(${TARGET} INTERFACE
  ${CMAKE_PROJECT_NAME}::types
  ${CMAKE_PROJECT_NAME}::math
)
