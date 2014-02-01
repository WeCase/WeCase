do_substitution = sed -e 's,[@]BINDIR[@],$(bindir),g'

wecase.desktop: wecase.desktop.in Makefile
	$(do_substitution) < $(srcdir)/wecase.desktop.in > wecase.desktop
	chmod +x wecase.desktop

appicondir = $(datadir)/icons/hicolor/96x96/apps
appicon_DATA = wecase.png

desktopdir = $(datadir)/applications
desktop_DATA = wecase.desktop

install-data-local:
	mkdir -p $(DESTDIR)$(pkgdatadir)/faces
	cp -R $(srcdir)/img/face/* $(DESTDIR)$(pkgdatadir)/faces

uninstall-local:
	rm -rf $(DESTDIR)$(pkgdatadir)/faces
