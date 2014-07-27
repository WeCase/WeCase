#AC_CONFIG_MACRO_DIRS([m4])
m4_include([m4/AC_PYTHON_MODULE.m4])
m4_include([m4/acx.m4])

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

AC_CHECK_PROG(PYUIC4_CHECK, pyuic4, yes)
if test x"$PYUIC4_CHECK" != x"yes" ; then
    AC_MSG_ERROR([Could not find pyuic4. Please install the development tools of PyQt4.])
fi

AC_CHECK_PROG(PYRCC4_CHECK, pyrcc4, yes)
if test x"$PYRCC4_CHECK" != x"yes" ; then
    AC_MSG_ERROR([Could not find pyrcc4. Please install the development tools of PyQt4.])
fi

ACX_CHECK_LRELEASE()

ACX_GIT_COMMIT_SHA1()
ACX_PKGPROVIDER([WeCase Developers])
ACX_BUGURL([http://bugs.wecase.org/])

AC_CONFIG_FILES([Makefile src/Makefile locale/Makefile res/Makefile])

AC_OUTPUT
