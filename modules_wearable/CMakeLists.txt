CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(dukgenerator C)

SET(PREFIX ${CMAKE_INSTALL_PREFIX})
SET(EXEC_PREFIX "\${prefix}")
SET(LIBDIR "\${prefix}/lib")
SET(INCLUDEDIR "\${prefix}/include")

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/inc)

SET(pc_requires " cryptsvc ")

INCLUDE(FindPkgConfig)
pkg_check_modules(pkgs REQUIRED ${pc_requires})

FOREACH(flag ${pkgs_CFLAGS})
	SET(EXTRA_CFLAGS "${EXTRA_CFLAGS} ${flag}")
ENDFOREACH(flag)

SET(source_dir "./src")
SET(include_dir "./inc")

SET(EXTRA_CFLAGS "${EXTRA_CFLAGS} -fvisibility=hidden")
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${EXTRA_CFLAGS}")
SET(EXTRA_CXXFLAGS "${EXTRA_CXXFLAGS} ${EXTRA_CFLAGS}")

##################################################################################################################
SET(SRCS
	${source_dir}/dukgen.c
)

SET(libcryptsvc_LDFLAGS " -module -avoid-version ${pkgs_LDFLAGS} ")
SET(libcryptsvc_CFLAGS " ${CFLAGS} -fvisibility=hidden -g -fPIC -I${CMAKE_CURRENT_SOURCE_DIR}/inc ")
SET(libcryptsvc_CPPFLAGS " -DPIC ")

#ADD_LIBRARY(${PROJECT_NAME} SHARED ${SRCS})
ADD_LIBRARY(${PROJECT_NAME} ${SRCS})
TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${pkgs_LDFLAGS})
SET_TARGET_PROPERTIES(
	${PROJECT_NAME}
	PROPERTIES
	VERSION ${FULLVER}
	SOVERSION ${MAJORVER}
)
##################################################################################################################

FIND_PROGRAM(UNAME NAMES uname)
EXEC_PROGRAM("${UNAME}" ARGS "-m" OUTPUT_VARIABLE "ARCH")
IF("${ARCH}" STREQUAL "arm")
	ADD_DEFINITIONS("-DTARGET")
	MESSAGE("add -DTARGET")
ENDIF("${ARCH}" STREQUAL "arm")

SET(PC_NAME ${PROJECT_NAME})
SET(PC_DESCRIPTION ${DESCRIPTION})
SET(PC_LDFLAGS -l${PROJECT_NAME})
SET(PC_REQUIRED ${pc_requires})
CONFIGURE_FILE(${PROJECT_NAME}.pc.in ${PROJECT_NAME}.pc @ONLY)

INSTALL(FILES ${PROJECT_NAME}.pc DESTINATION lib/pkgconfig)
INSTALL(TARGETS ${PROJECT_NAME} DESTINATION lib)
INSTALL(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/inc/ DESTINATION /usr/include)

ADD_DEFINITIONS(-D_bool_cryptsvc)
