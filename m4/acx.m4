dnl Support the --with-pkgprovider configure option.
dnl ACX_PKGVERSION(default-pkgprovider)
AC_DEFUN([ACX_PKGPROVIDER],[
  AC_ARG_WITH(pkgprovider,
    AS_HELP_STRING([--with-pkgprovider=ORGANIZATION],
                   [Use ORGANIZATION in the provider string in place of "$1"]),
    [case "$withval" in
      yes) AC_MSG_ERROR([package provider not specified]) ;;
      no)  PKGPROVIDER= ;;
      *)   PKGPROVIDER="$withval" ;;
     esac],
    PKGPROVIDER="$1"
    DEFAULTPROVIDER="$1"
  )
  AC_SUBST(PKGPROVIDER)
  AC_SUBST(DEFAULTPROVIDER)
])


dnl Support the --with-bugurl configure option.
dnl ACX_BUGURL(default-bugurl)
AC_DEFUN([ACX_BUGURL],[
  AC_ARG_WITH(bugurl,
    AS_HELP_STRING([--with-bugurl=URL],
                   [Direct users to URL to report a bug]),
    [case "$withval" in
      yes) AC_MSG_ERROR([bug URL not specified]) ;;
      no)  BUGURL=
           ;;
      *)   BUGURL="$withval"
           ;;
     esac],
     BUGURL="$1"
  )
  case ${BUGURL} in
  "")
    REPORT_BUGS_TO=
    ;;
  *)
    REPORT_BUGS_TO="<$BUGURL>"
    ;;
  esac;
  AC_SUBST(REPORT_BUGS_TO)
])


AC_DEFUN([ACX_GIT_COMMIT_SHA1],[
    AC_MSG_CHECKING(for Git commit SHA1)
    GIT_COMMIT_SHA1=$(git rev-parse --short HEAD 2> /dev/null)
    if test $? -eq 0;
    then
        :
    else
        GIT_COMMIT_SHA1="unknown"
    fi

    git ls-files --other --error-unmatch . >/dev/null 2>&1
    status=$?
    if test "$status" = 0; then
        GIT_COMMIT_SHA1="${GIT_COMMIT_SHA1}-dirty"
    elif test "$status" = 1; then
        :
    else
        :
    fi

    AC_MSG_RESULT($GIT_COMMIT_SHA1)
    AC_SUBST(GIT_COMMIT_SHA1)
])
