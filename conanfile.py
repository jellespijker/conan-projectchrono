from conans import ConanFile, CMake, tools
import os

class ProjectChronoConan(ConanFile):
    name = "projectchrono"
    version = "5.0.1"
    description = "C++ library for multi-physics simulation"
    topics = ("chronoengine", "project chrono", "multi-physics simulation", "DEM", "FSI", "vehicle", "simulation")
    url = "https://github.com/jellespijker/conan-projectchrono"
    homepage = "https://github.com/projectchrono/chrono"
    license = "AGPL3"
    # exports_sources = ["CMakeLists.txt", "patches/*.patch"]
    generators = "cmake"  #, "cmake_find_package", "cmake_paths"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "openMP": ["On", "Off"],
               "TBB": ["On", "Off"],
               "HDF5": ["On", "Off"],
               "benchmarking": ["On", "Off"],
               "demos": ["On", "Off"],
               "tests": ["On", "Off"],
               "unit_cascade": ["On", "Off"],  # Not yet implemented
               "module_cosimulation": ["On", "Off"],
               "module_distributed": ["On", "Off"],
               "module_irrlicht": ["On", "Off"],
               "module_matlab": ["On", "Off"],
               "module_mkl": ["On", "Off"],  #  Not yet implemented
               "module_mumps": ["On", "Off"],  # Not yet implemented
               "module_parallel": ["On", "Off"],
               "module_opengl": ["On", "Off"],
               "module_ogre": ["On", "Off"],
               "module_postprocess": ["On", "Off"],
               "module_python": ["On", "Off"],
               "module_vehicle": ["On", "Off"],
               "module_fsi": ["On", "Off"],
               "use_bullet_double": ["On", "Off"],
               "module_granular": ["On", "Off"],
               "use_parallel_cuda": ["On", "Off"],  # Not yet implemented
               "use_parallel_double": ["On", "Off"]}
    default_options = {"shared": True,
                       "fPIC": True,
                       "openMP": "Off",
                       "TBB": "On",
                       "HDF5": "Off",
                       "benchmarking": "Off",
                       "demos": "Off",
                       "tests": "Off",
                       "unit_cascade": "Off",
                       "module_cosimulation": "Off",
                       "module_distributed": "Off",
                       "module_irrlicht": "On",
                       "module_matlab": "Off",
                       "module_mkl": "Off",
                       "module_mumps": "Off",
                       "module_parallel": "Off",
                       "module_opengl": "Off",
                       "module_ogre": "Off",
                       "module_postprocess": "Off",
                       "module_python": "Off",
                       "module_vehicle": "Off",
                       "module_fsi": "Off",
                       "use_bullet_double": "Off",
                       "module_granular": "Off",
                       "use_parallel_cuda": "Off",
                       "use_parallel_double": "On"}

    _source_subfolder = "src"
    _build_folder = "build"
    _cmake = None

    scm = {
        "type": "git",
        "subfolder":_source_subfolder,
        "url": "https://github.com/projectchrono/chrono.git",
        "revision": version,
        "submodule": "recursive"
    }

    def source(self):
        tools.replace_in_file("src/CMakeLists.txt", "project(Chrono VERSION ${CHRONO_VERSION_MAJOR}.${CHRONO_VERSION_MINOR}.${CHRONO_VERSION_PATCH})",
                              '''project(Chrono VERSION ${CHRONO_VERSION_MAJOR}.${CHRONO_VERSION_MINOR}.${CHRONO_VERSION_PATCH})
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.options.openMP == "On":  # and str(self.settings.compiler) == 'clang':
            self.requires.add("llvm-openmp/10.0.0")
        if self.options.TBB == "On":
            self.requires.add("tbb/2020.1")
        self.requires.add("zlib/1.2.11")
        self.requires.add("openmpi/3.1.2@jellespijker/testing")
        self.requires.add("eigen/3.3.7@conan/stable")
        if self.options.HDF5 == "On":
            self.requires.add("hdf5/1.12.0")
        if self.options.module_irrlicht == "On":
            self.requires.add("irrlicht/1.8.4@jellespijker/testing")
        if self.options.module_mumps == "On":
            # self.requires.add("mumps")
            self.requires.add("openblas/0.3.10")
        if self.options.module_opengl == "On":
            self.requires.add("opengl/system")
            self.requires.add("glm/0.9.9.8")
            self.requires.add("glew/2.1.0")
            self.requires.add("glfw/3.3.2")
        if self.options.module_parallel == "On":
            self.requires.add("thrust/1.9.5")
            self.requires.add("blaze/3.7")
        if self.options.module_python == "On":
            self.requires.add("swig/4.0.1")


    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["BUILD_DEMOS"] = self.options.demos
            self._cmake.definitions["BUILD_BENCHMARKING"] = self.options.benchmarking
            self._cmake.definitions["ENABLE_OPENMP"] = self.options.openMP
            self._cmake.definitions["ENABLE_TBB"] = self.options.TBB
            self._cmake.definitions["ENABLE_HDF5"] = self.options.HDF5
            self._cmake.definitions["BUILD_TESTING"] = self.options.tests
            self._cmake.definitions["ENABLE_UNIT_CASCADE"] = self.options.unit_cascade
            self._cmake.definitions["ENABLE_MODULE_COSIMULATION"] = self.options.module_cosimulation
            self._cmake.definitions["ENABLE_MODULE_DISTRIBUTED"] = self.options.module_distributed
            self._cmake.definitions["ENABLE_MODULE_IRRLICHT"] = self.options.module_irrlicht
            self._cmake.definitions["ENABLE_MODULE_MATLAB"] = self.options.module_matlab
            self._cmake.definitions["ENABLE_MODULE_MKL"] = self.options.module_mkl
            self._cmake.definitions["ENABLE_MODULE_MUMPS"] = self.options.module_mumps
            self._cmake.definitions["ENABLE_MODULE_PARALLEL"] = self.options.module_parallel
            self._cmake.definitions["ENABLE_MODULE_OPENGL"] = self.options.module_opengl
            self._cmake.definitions["ENABLE_MODULE_OGRE"] = self.options.module_ogre
            self._cmake.definitions["ENABLE_MODULE_POSTPROCESS"] = self.options.module_postprocess
            self._cmake.definitions["ENABLE_MODULE_PYTHON"] = self.options.module_python
            self._cmake.definitions["ENABLE_MODULE_VEHICLE"] = self.options.module_vehicle
            self._cmake.definitions["ENABLE_MODULE_FSI"] = self.options.module_fsi
            self._cmake.definitions["ENABLE_MODULE_GRANULAR"] = self.options.module_granular
        self._cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_folder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

