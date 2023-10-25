cmake_minimum_required(VERSION 3.18)

project(typeStructure)

include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1  # Adjust the version as needed
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(TypeStructureLib src/bind.cpp)

target_include_directories(TypeStructureLib PUBLIC inc)
