#AC_CONFIG_MACRO_DIRS([m4])
m4_include([m4/AC_PYTHON_MODULE.m4])
m4_include([m4/acx.m4])
m4_include([m4/pyqt4.m4])

AC_INIT([WeCase], [0.06-beta8])

AM_INIT_AUTOMAKE
AM_PATH_PYTHON([3.2],, AC_MSG_ERROR(Could not find Python >= 3.2.))

AC_PYTHON_MODULE([PyQt4])
if test $HAVE_PYMOD_PYQT4 = "no"; then
    AC_MSG_ERROR(Could not find Python module PyQt4.)
fi

AC_PYTHON_MODULE([rpweibo])
if test $HAVE_PYMOD_RPWEIBO = "no"; then
    AC_MSG_ERROR(Could not find Python module rpweibo.)
fi

AC_PYTHON_MODULE([notify2])
if test $HAVE_PYMOD_NOTIFY2 = "no"; then
    AC_MSG_WARN(Could not find Python module notify2, notification is unavaliable.)
fi

AC_CHECK_QT4_TOOLS()
AC_CHECK_PYQT4_TOOLS()

ACX_GIT_COMMIT_SHA1()
ACX_PKGPROVIDER([WeCase Developers])
ACX_BUGURL([http://bugs.wecase.org/])

AC_CONFIG_FILES([Makefile src/Makefile locale/Makefile res/Makefile])

AC_OUTPUT
