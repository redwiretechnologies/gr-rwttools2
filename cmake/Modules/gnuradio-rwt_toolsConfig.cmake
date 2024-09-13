find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_RWT_TOOLS gnuradio-rwt_tools)

FIND_PATH(
    GR_RWT_TOOLS_INCLUDE_DIRS
    NAMES gnuradio/rwt_tools/api.h
    HINTS $ENV{RWT_TOOLS_DIR}/include
        ${PC_RWT_TOOLS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_RWT_TOOLS_LIBRARIES
    NAMES gnuradio-rwt_tools
    HINTS $ENV{RWT_TOOLS_DIR}/lib
        ${PC_RWT_TOOLS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-rwt_toolsTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_RWT_TOOLS DEFAULT_MSG GR_RWT_TOOLS_LIBRARIES GR_RWT_TOOLS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_RWT_TOOLS_LIBRARIES GR_RWT_TOOLS_INCLUDE_DIRS)
