import re
import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, load
from conan.tools.scm import Git

class Conan(ConanFile):
    name = "cppql"
    description = "C++ sqlite library."
    url = "https://github.com/TimZoet/cppql"
    author = "Tim Zoet"
    package_type = "static-library"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "fPIC": [True, False],
        "zero_based_indices": [True, False],
        "shutdown_default_off": [True, False]
    }
    
    default_options = {
        "fPIC": True,
        "zero_based_indices": True,
        "shutdown_default_off": False
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def configure(self):
        pass
    
    def source(self):
        data = self.conan_data["sources"][self.version]
        git = Git(self)
        git.clone(url=data["url"], target=".", args=["--recurse-submodules"])

    def layout(self):
        cmake_layout(self, src_folder="src")
    
    def requirements(self):
        self.requires("common/2.0.0")
        self.requires("sqlite3/3.49.1")
    
    def generate(self):
        tc = CMakeToolchain(self)

        tc.cache_variables["CPPQL_BIND_ZERO_BASED_INDICES"] = self.options.zero_based_indices
        tc.cache_variables["CPPQL_SHUTDOWN_DEFAULT_OFF"] = self.options.shutdown_default_off

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
        self.cpp_info.components["cppql"].libs = ["cppql"]
        self.cpp_info.components["cppql"].requires = ["common::common", "sqlite3::sqlite"]
