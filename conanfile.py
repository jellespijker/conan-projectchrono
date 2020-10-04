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
    generators = "cmake", "cmake_find_package", "cmake_paths"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "openMP": [True, False],
               "TBB": [True, False],
               "HDF5": [True, False],
               "benchmarking": [True, False],
               "demos": [True, False],
               "tests": [True, False],
               "unit_cascade": [True, False],  # Not yet implemented
               "module_cosimulation": [True, False],
               "module_distributed": [True, False],
               "module_irrlicht": [True, False],
               "module_matlab": [True, False],
               "module_mkl": [True, False],  #  Not yet implemented
               "module_mumps": [True, False],  # Not yet implemented
               "module_parallel": [True, False],
               "module_opengl": [True, False],
               "module_ogre": [True, False],
               "module_postprocess": [True, False],
               "module_python": [True, False],
               "module_vehicle": [True, False],
               "module_fsi": [True, False],
               "use_bullet_double": [True, False],
               "module_granular": [True, False],
               "use_parallel_cuda": [True, False],  # Not yet implemented
               "use_parallel_double": [True, False]}
    default_options = {"shared": True,
                       "fPIC": True,
                       "openMP": False,
                       "TBB": True,
                       "HDF5": False,
                       "benchmarking": False,
                       "demos": False,
                       "tests": False,
                       "unit_cascade": False,
                       "module_cosimulation": False,
                       "module_distributed": False,
                       "module_irrlicht": False,
                       "module_matlab": False,
                       "module_mkl": False,
                       "module_mumps": False,
                       "module_parallel": False,
                       "module_opengl": False,
                       "module_ogre": False,
                       "module_postprocess": False,
                       "module_python": False,
                       "module_vehicle": False,
                       "module_fsi": False,
                       "use_bullet_double": False,
                       "module_granular": False,
                       "use_parallel_cuda": False,
                       "use_parallel_double": True}

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
conan_basic_setup()
include_directories(CONAN_INCLUDE_DIRS_IRRLICHT)''')

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.options.openMP:  # and str(self.settings.compiler) == 'clang':
            self.requires.add("llvm-openmp/10.0.0")
        if self.options.TBB:
            self.requires.add("tbb/2020.1")
        self.requires.add("zlib/1.2.11")
        self.requires.add("openmpi/3.1.2@jellespijker/testing")
        self.requires.add("eigen/3.3.7")
        if self.options.HDF5:
            self.requires.add("hdf5/1.12.0")
        if self.options.module_irrlicht:
            self.requires.add("irrlicht/1.8.4@jellespijker/testing")
            self.requires.add("openssl/1.1.1g")
        if self.options.module_mumps:
            # self.requires.add("mumps")
            self.requires.add("openblas/0.3.10")
        if self.options.module_opengl:
            self.requires.add("opengl/system")
            self.requires.add("glm/0.9.9.8")
            self.requires.add("glew/2.1.0")
            self.requires.add("glfw/3.3.2")
        if self.options.module_parallel:
            self.requires.add("thrust/1.9.5")
            self.requires.add("blaze/3.7")
        if self.options.module_python:
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

