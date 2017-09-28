cmake_minimum_required(VERSION 3.7)
project(libStub)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES library.cpp library.h)
add_library(libStub SHARED ${SOURCE_FILES})