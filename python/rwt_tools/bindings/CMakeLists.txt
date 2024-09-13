# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT rwt_tools_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT rwt_tools_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND rwt_tools_python_files
    corr_est_ff_python.cc
    tx_burst_tagger_cc_python.cc
    zero_pad_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(rwt_tools
   ../../..
   gr::rwt_tools
   "${rwt_tools_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET rwt_tools_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:rwt_tools_python>
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/rwt_tools/
)

install(TARGETS rwt_tools_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/rwt_tools COMPONENT pythonapi)
