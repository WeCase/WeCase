do_substitution = sed -e 's,[@]BINDIR[@],$(bindir),g'

wecase.desktop: wecase.desktop.in Makefile
	$(do_substitution) < $(srcdir)/wecase.desktop.in > wecase.desktop
	chmod +x wecase.desktop

appicondir = $(datadir)/icons/hicolor/96x96/apps
appicon_DATA = wecase.png

desktopdir = $(datadir)/applications
desktop_DATA = wecase.desktop

install-data-local:
	cp -R $(srcdir)/img/face $(datadir)/face

uninstall-local:
	rm -rf $(datadir)/face
