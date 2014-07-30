AC_DEFUN([AC_CHECK_QT4_TOOLS], [
    dnl lrelease
    m4_define_default(
        [_QT4_LRELEASE_NAME], [lrelease-qt4 lrelease])
    AC_ARG_VAR([LRELEASE], [the Qt4 Linguist compiler])

    if test -z "$LRELEASE"; then
        AC_PATH_PROGS([LRELEASE], _QT4_LRELEASE_NAME, :)
    else
        LRELEASE=$(readlink -f $LRELEASE)
    fi
    if test "$LRELEASE" = :; then
        AC_MSG_ERROR([no suitable Qt4 Linguist compiler found])
    fi
    AC_SUBST(LRELEASE)
])

AC_DEFUN([AC_CHECK_PYQT4_TOOLS], [
    dnl pyuic4
    m4_define_default(
        [_PYQT4_PYUIC4_NAME], [pyuic4-python3 pyuic4])

    AC_ARG_VAR([PYUIC4], [the PyQt4 UI compiler])

    if test -z "$PYUIC4"; then
        AC_PATH_PROGS([PYUIC4], _PYQT4_PYUIC4_NAME, :)
    else
        PYUIC4=$(readlink -f $PYUIC4)
    fi
    if test "$PYUIC4" = :; then
        AC_MSG_ERROR([no suitable PyQt4 UI compiler found])
    fi
    AC_SUBST(PYUIC4)

    dnl pyrcc4
    m4_define_default(
        [_PYQT4_PYRCC4_NAME], [pyrcc4])

    AC_ARG_VAR([PYRCC4], [the PyQt4 resource compiler])

    if test -z "$PYRCC4"; then
        AC_PATH_PROGS([PYRCC4], _PYQT4_PYRCC4_NAME, :)
    else
        PYRCC4=$(readlink -f $PYRCC4)
    fi
    if test "$PYRCC4" = :; then
        AC_MSG_ERROR([no suitable PyQt4 resource compiler found])
    fi
    AC_SUBST(PYRCC4)
])
