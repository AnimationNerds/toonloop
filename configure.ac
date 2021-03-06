#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT(TOONLOOP, 2.2.2, [support@toonloop.com], [toonloop], [http://www.toonloop.com])
AC_CONFIG_HEADER([src/config.h])
AC_CONFIG_MACRO_DIR([m4]) # check for m4 macros in directory m4
AC_PROG_LIBTOOL
AM_INIT_AUTOMAKE()

AS_VERSION
AC_DEFINE_UNQUOTED(PACKAGE_VERSION_MAJOR, $PACKAGE_VERSION_MAJOR, [major version])
AC_DEFINE_UNQUOTED(PACKAGE_VERSION_MINOR, $PACKAGE_VERSION_MINOR, [minor version])
AC_DEFINE_UNQUOTED(PACKAGE_VERSION_MICRO, $PACKAGE_VERSION_MICRO, [micro version])

# Check for C++ compiler
AC_PROG_CXX

# check for programs
AC_PROG_INSTALL
AC_PROG_LN_S

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([arpa/inet.h stdlib.h string.h sys/ioctl.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_CONST
PKG_PROG_PKG_CONFIG

AC_PROG_GCC_TRADITIONAL
AC_CHECK_FUNCS([inet_ntoa memset socket])

AC_CHECK_LIB([pthread],[pthread_exit],[AC_SUBST([LIBTHREAD_CXXFLAGS],["-lpthread"])])
AC_CHECK_LIB([m],[sin],[AC_SUBST([LIBM_CXXFLAGS],["-lm"])])

# check for the RTMIDI
PKG_CHECK_MODULES([RTMIDI], [rtmidi], have_rtmidi=true, have_rtmidi=false)
if test "x${have_rtmidi}" = "xfalse" ; then
    AC_MSG_ERROR([Missing librtmidi-dev])
fi

#Set LIBLO with pkg-config
PKG_CHECK_MODULES(LIBLO, liblo, have_liblo=true, have_liblo=false)
if test "x${have_liblo}" = "xfalse" ; then
    AC_MSG_ERROR([Missing liblo])
fi

# GST
PKG_CHECK_MODULES([GST], [gstreamer-0.10 >= 0.10.0 gstreamer-interfaces-0.10 >= 0.10.19])
AC_SUBST([GST_LIBS])
AC_SUBST([GST_CFLAGS])

# GST appsink 
PKG_CHECK_MODULES(GSTAPP, gstreamer-app-0.10, have_gstreamer_app=true, have_gstreamer_app=false)
if test "x${have_gstreamer_app}" = "xfalse" ; then
    AC_MSG_ERROR([missing package: libgstreamer-plugins-base0.10-dev])
fi
AC_SUBST([GSTAPP_LIBS])

# Clutter
PKG_CHECK_MODULES([CLUTTER], [clutter-1.0 >= 1.0], have_clutter=true, have_clutter=false)
if test "x${have_clutter}" = "xfalse" ; then
    AC_MSG_ERROR([missing package: libclutter])
fi
AC_SUBST([CLUTTER_LIBS])
AC_SUBST([CLUTTER_CFLAGS])
# Clutter depends on:
# libjson-glib-dev and others

# Clutter-GST
PKG_CHECK_MODULES([CLUTTERGST], [clutter-gst-1.0 >= 1.0], have_clutter_gst=true, 
    PKG_CHECK_MODULES([CLUTTERGST], [clutter-gst-0.10 >= 0.10], have_clutter_gst=true, have_clutter_gst=false))
if test "x${have_clutter_gst}" = "xfalse" ; then
    AC_MSG_ERROR([missing package: libclutter-gst-dev])
fi
AC_SUBST([CLUTTERGST_LIBS])
AC_SUBST([CLUTTERGST_CFLAGS])

#Set libraw1394 with pkg-config
PKG_CHECK_MODULES(RAW1394, libraw1394, have_raw1394=true, have_raw1394=false)
if test "x${have_raw1394}" = "xfalse" ; then
    AC_MSG_ERROR([Missing libraw1394])
fi

#Trying to set LIBAVC1394 using pkg-config
PKG_CHECK_MODULES(AVC1394, [libavc1394], have_avc1394=true, have_avc1394=false)
if test "x${have_avc1394}" = "xfalse" ; then
	AC_MSG_ERROR([missing package: libavc1394-dev ])
fi

# libxml2
PKG_CHECK_MODULES([LIBXML], [libxml-2.0], have_libxml=true, have_libxml=false)
if test "x${have_libxml}" = "xfalse" ; then
    AC_MSG_ERROR([missing package: libxml2-dev])
fi
AC_SUBST([LIBXML_LIBS])
AC_SUBST([LIBXML_CFLAGS])

# BOOST
AX_BOOST_BASE([1.35])

AX_BOOST_PROGRAM_OPTIONS
if test "x${ax_cv_boost_program_options}" = "xno" ; then
	AC_MSG_ERROR([missing package: libboost-program-options-dev])
fi

AX_BOOST_FILESYSTEM
if test "x${ax_cv_boost_filesystem}" = "xno" ; then
	AC_MSG_ERROR([missing package: libboost-filesystem-dev])
fi

AX_BOOST_THREAD
if test "x${ax_cv_boost_thread}" = "xno" ; then
    AC_MSG_ERROR([missing package: libboost-thread-dev])
fi

AX_BOOST_DATE_TIME
if test "x${ax_cv_boost_date_time}" = "xno" ; then
	AC_MSG_ERROR([missing package: libboost-date-time-dev])
fi

AX_BOOST_SYSTEM
if test "x${ax_cv_boost_system}" = "xno" ; then
	AC_MSG_ERROR([missing package: libboost-system-dev])
fi

# GNU help2man creates man pages from --help output; in many cases, this
# is sufficient, and obviates the need to maintain man pages separately.
# However, this means invoking executables, which we generally cannot do
# when cross-compiling, so we test to avoid that (the variable
# "cross_compiling" is set by AC_PROG_CC).
if test $cross_compiling = no; then
    AM_MISSING_PROG(HELP2MAN, help2man)
else
    HELP2MAN=:
fi

AS_AC_EXPAND(DATADIR, $datadir)
AC_MSG_NOTICE(Storing data files in $DATADIR)

PIXMAPS_DIR=$DATADIR/pixmaps
AC_SUBST(PIXMAPS_DIR)
AC_MSG_NOTICE(Storing pixmaps files in $PIXMAPS_DIR)

AC_DEFINE_UNQUOTED([DATADIR], "${DATADIR}", "Data dir")
AC_DEFINE_UNQUOTED([PIXMAPS_DIR], "${PIXMAPS_DIR}", "Pixmaps dir")

AC_SUBST(CXXFLAGS, " -O2 -Wall -Wextra -Wno-unused-result -Wfatal-errors") dnl -Werror 
AC_CONFIG_FILES([
    Makefile
    src/Makefile
    src/doxyfile
    src/shaders/Makefile
    man/Makefile
    tests/Makefile
    pixmaps/Makefile
    completion/Makefile
    presets/Makefile
    ])
AC_OUTPUT

