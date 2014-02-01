bin_SCRIPTS = wecase
libexec_SCRIPTS = wecase.py
CLEANFILES = path.py wecase wecase.py

NAME = WeCase

do_substitution = sed -e 's,[@]DATADIR[@],$(datadir),g' \
				  -e 's,[@]LOCALEDIR[@],$(localedir)/$(NAME),g' \
				  -e 's,[@]PACKAGE[@],$(PACKAGE),g' \
			      -e 's,[@]PYTHONDIR[@],$(pythondir)/$(NAME),g' \
				  -e 's,[@]LIBEXECDIR[@],$(libexecdir),g'

path.py: path.py.in Makefile
	$(do_substitution) < $(srcdir)/path.py.in > path.py

wecase.py: wecase.py.in Makefile
	$(do_substitution) < $(srcdir)/wecase.py.in > wecase.py

wecase: wecase.in Makefile
	$(do_substitution) < $(srcdir)/wecase.in > wecase
	chmod +x wecase

AboutWindow_ui.py:
	pyuic4 $(srcdir)/../res/ui/AboutWindow.ui > AboutWindow_ui.py

LoginWindow_ui.py:
	pyuic4 $(srcdir)/../res/ui/LoginWindow.ui > LoginWindow_ui.py

NewpostWindow_ui.py:
	pyuic4 $(srcdir)/../res/ui/NewpostWindow.ui > NewpostWindow_ui.py

SettingWindow_ui.py:
	pyuic4 $(srcdir)/../res/ui/SettingWindow.ui > SettingWindow_ui.py

wecase_rc.py:
	pyrcc4 $(srcdir)/../res/ui/wecase.qrc -py3 -compress 9 > wecase_rc.py

WeCasedir = $(pythondir)/WeCase
WeCase_PYTHON = path.py \
				AboutWindow.py \
				const.py \
				Face.py \
				FaceWidget.py \
				FaceWindow.py \
				LoginWindow.py \
				NewpostWindow.py \
				Notify.py \
				nullNotify.py \
				SettingWindow.py \
				TweetListWidget.py \
				Tweet.py \
				TweetUtils.py \
				TweetUtils_test.py \
				WAsyncLabel.py \
				WAvatarLabel.py \
				WCompleteLineEdit.py \
				WeCaseWindow.py \
				WeHack.py \
				WeRuntimeInfo.py \
				WIconLabel.py \
				WImageLabel.py \
				WObjectCache.py \
				WSwitchLabel.py \
				WTimeParser.py \
				WTimeParser_test.py \
				WTimer.py \
				WTweetLabel.py \
				WConfigParser.py \
				FilterTable.py \
				WeiboErrorHandler.py \
				AboutWindow_ui.py \
				LoginWindow_ui.py \
				NewpostWindow_ui.py \
				SettingWindow_ui.py \
				wecase_rc.py


Weibosdir = $(pythondir)/WeCase/weibos

Weibos_PYTHON = weibos/client.py \
				weibos/helper.py \
				weibos/__init__.py

metaconfdir = $(pythondir)/WeCase/
metaconf_DATA = WMetaConfig
