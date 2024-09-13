# Copyright 2020 Red Wire Technologies.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

list(APPEND rwt_tools_sources
    corr_est_ff_impl.cc
    tx_burst_tagger_cc_impl.cc
    zero_pad_impl.cc
)

set(rwt_tools_sources "${rwt_tools_sources}" PARENT_SCOPE)
if(NOT rwt_tools_sources)
    MESSAGE(STATUS "No C++ sources... skipping lib/")
    return()
endif(NOT rwt_tools_sources)

add_library(gnuradio-rwt_tools SHARED ${rwt_tools_sources})
target_link_libraries(gnuradio-rwt_tools gnuradio::gnuradio-runtime 
    gnuradio::gnuradio-blocks gnuradio::gnuradio-fft gnuradio::gnuradio-filter
    gnuradio::gnuradio-digital)
target_include_directories(gnuradio-rwt_tools
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
    PUBLIC $<INSTALL_INTERFACE:include>
  )
set_target_properties(gnuradio-rwt_tools PROPERTIES DEFINE_SYMBOL "gnuradio_rwt_tools_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-rwt_tools PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-rwt_tools)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

# If your unit tests require special include paths, add them here
#include_directories()
# List all files that contain Boost.UTF unit tests here
list(APPEND test_rwt_tools_sources
)
# Anything we need to link to for the unit tests go here
list(APPEND GR_TEST_TARGET_DEPS gnuradio-rwt_tools)

if(NOT test_rwt_tools_sources)
    MESSAGE(STATUS "No C++ unit tests... skipping")
    return()
endif(NOT test_rwt_tools_sources)

foreach(qa_file ${test_rwt_tools_sources})
    GR_ADD_CPP_TEST("rwt_tools_${qa_file}"
        ${CMAKE_CURRENT_SOURCE_DIR}/${qa_file}
    )
endforeach(qa_file)
