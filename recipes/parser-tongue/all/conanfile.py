import re
import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, load
from conan.tools.scm import Git

class Conan(ConanFile):
    name = "parser-tongue"
    description = "C++ utilities."
    url = "https://github.com/TimZoet/parser-tongue"
    author = "Tim Zoet"
    package_type = "static-library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False]
    }
    default_options = {
        "fPIC": True
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
    
    def generate(self):
        tc = CMakeToolchain(self)
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
        self.cpp_info.components["parser-tongue"].libs = ["parser-tongue"]
