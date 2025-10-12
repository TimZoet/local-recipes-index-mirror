import re
import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, load
from conan.tools.scm import Git

class Conan(ConanFile):
    name = "better-test"
    description = "C++ testing framework."
    url = "https://github.com/TimZoet/better-test"
    author = "Tim Zoet"
    package_type = "static-library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "build_alexandria": [True, False],
        "build_json": [True, False],
        "build_xml": [True, False]
    }
    
    default_options = {
        "fPIC": True,
        "build_alexandria": False,
        "build_json": False,
        "build_xml": False
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
        self.requires("common/2.0.0", transitive_headers=True)
        self.requires("date/3.0.1")
        self.requires("parser-tongue/2.0.0")
        if self.options.build_alexandria:
            self.requires("alexandria/2.0.0")
        if self.options.build_json:
            self.requires("nlohmann_json/3.9.1")
        if self.options.build_xml:
            self.requires("pugixml/1.11")
    
    def generate(self):
        tc = CMakeToolchain(self)

        tc.cache_variables["BETTERTEST_BUILD_ALEXANDRIA"] = self.options.build_alexandria
        tc.cache_variables["BETTERTEST_BUILD_JSON"] = self.options.build_json
        tc.cache_variables["BETTERTEST_BUILD_XML"] = self.options.build_xml

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
        self.cpp_info.components["core"].libs = ["bettertest"]
        self.cpp_info.components["core"].requires = ["common::common", "date::date", "parser-tongue::parser-tongue"]
        if self.options.build_alexandria:
            self.cpp_info.components["alexandria"].libs = ["bettertest-alexandria"]
            self.cpp_info.components["alexandria"].requires = ["core", "alexandria::alexandria"]
            self.cpp_info.components["alexandria"].defines = ["BETTERTEST_BUILD_ALEXANDRIA"]
        if self.options.build_json:
            self.cpp_info.components["json"].libs = ["bettertest-json"]
            self.cpp_info.components["json"].requires = ["core", "nlohmann_json::nlohmann_json"]
            self.cpp_info.components["json"].defines = ["BETTERTEST_BUILD_JSON"]
        if self.options.build_xml:
            self.cpp_info.components["xml"].libs = ["bettertest-xml"]
            self.cpp_info.components["xml"].requires = ["core", "pugixml::pugixml"]
            self.cpp_info.components["xml"].defines = ["BETTERTEST_BUILD_XML"]
