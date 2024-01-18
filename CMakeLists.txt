cmake_minimum_required(VERSION 3.27)
project(lab)

set(CMAKE_CXX_STANDARD 20)

add_executable(lab main.cpp)

add_subdirectory(lib/ips4o)
target_link_libraries(lab PRIVATE ips4o)