import re
import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, load
from conan.tools.scm import Git

class Conan(ConanFile):
    name = "math"
    description = "..."
    url = "https://github.com/TimZoet/math"
    author = "Tim Zoet"
    package_type = "header-library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "enable_sse41": [True, False],
        "enable_sse42": [True, False],
        "enable_avx": [True, False],
        "enable_avx2": [True, False],
        "enable_fma": [True, False]
    }
    default_options = {
        "enable_sse41": False,
        "enable_sse42": False,
        "enable_avx": False,
        "enable_avx2": False,
        "enable_fma": False
    }

    def config_options(self):
        pass
    
    def configure(self):
        pass
    
    def source(self):
        data = self.conan_data["sources"][self.version]
        git = Git(self)
        git.clone(url=data["url"], target=".", args=["--recurse-submodules"])

    def layout(self):
        cmake_layout(self, src_folder="src")
    
    def requirements(self):
        pass
    
    def generate(self):
        tc = CMakeToolchain(self)

        if self.options.enable_sse41:
            tc.cache_variables["MATH_ENABLE_SSE41"] = True
            #tc.extra_cxxflags.append("-msse4.1")
        if self.options.enable_sse42:
            tc.cache_variables["MATH_ENABLE_SSE42"] = True
            #tc.extra_cxxflags.append("-msse4.2")
        if self.options.enable_avx:
            tc.cache_variables["MATH_ENABLE_AVX"] = True
            #tc.extra_cxxflags.append("-mavx")
        if self.options.enable_avx2:
            tc.cache_variables["MATH_ENABLE_AVX2"] = True
            #tc.extra_cxxflags.append("-mavx2")
        if self.options.enable_fma:
            tc.cache_variables["MATH_ENABLE_FMA"] = True
            #tc.extra_cxxflags.append("-mfma")

        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
    
    def package_info(self):
        self.cpp_info.components["math"].libs = ["math"]
        #if self.options.enable_sse41:
        #    self.cpp_info.components["math"].defines.append("__SSE4_1__")
        #    self.cpp_info.components["math"].cxxflags.append("-msse4.1")
        #if self.options.enable_sse42:
        #    self.cpp_info.components["math"].defines.append("__SSE4_2__")
        #    self.cpp_info.components["math"].cxxflags.append("-msse4.2")
        #if self.options.enable_avx:
        #    self.cpp_info.components["math"].defines.append("__AVX__")
        #    self.cpp_info.components["math"].cxxflags.append("-mavx")
        #if self.options.enable_avx2:
        #    self.cpp_info.components["math"].defines.append("__AVX2__")
        #    self.cpp_info.components["math"].cxxflags.append("-mavx2")
        #if self.options.enable_fma:
        #    self.cpp_info.components["math"].defines.append("__FMA__")
        #    self.cpp_info.components["math"].cxxflags.append("-mfma")
