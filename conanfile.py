from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools.cmake import CMakeToolchain


class BinderBenchmarkRecipe(ConanFile):
    name = "binder"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    def generate(self):
        tc = CMakeToolchain(self)
        # Generate python module
        # tc.variables["PYTHON_MODULE"] = True
        tc.generate()

    def requirements(self):
        # from ennui
        self.requires("eigen/3.4.0")
        self.requires("catch2/3.4.0")

    def build_requirements(self):
        # from ennui
        self.tool_requires("cmake/[>=3.20]")

    def layout(self):
        cmake_layout(self)
