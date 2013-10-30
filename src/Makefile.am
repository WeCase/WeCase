bin_SCRIPTS = path wecase.py
CLEANFILES = $(path) path.py wecase.py

NAME = WeCase

do_substitution = sed -e 's,[@]DATADIR[@],$(datadir),g' \
				  -e 's,[@]LOCALEDIR[@],$(localedir)/$(NAME),g' \
				  -e 's,[@]PACKAGE[@],$(name),g' \
			      -e 's,[@]PYTHONDIR[@],$(pythondir)/$(NAME),g'

path: path.py.in Makefile
	$(do_substitution) < $(srcdir)/path.py.in > path.py
	$(do_substitution) < $(srcdir)/wecase.py.in > wecase.py

WeCasedir = $(pythondir)/WeCase
WeCase_PYTHON = path.py \
				AboutWindow.py \
				AboutWindow_ui.py \
				const.py \
				Face.py \
				FaceWidget.py \
				FaceWindow.py \
				FaceWindow_ui.py \
				LoginWindow.py \
				LoginWindow_ui.py \
				make.py \
				NewpostWindow.py \
				NewpostWindow_ui.py \
				Notify.py \
				nullNotify.py \
				SettingWindow.py \
				SettingWindow_ui.py \
				TweetListWidget.py \
				Tweet.py \
				TweetUtils.py \
				TweetUtils_test.py \
				WAsyncLabel.py \
				WAvatarLabel.py \
				WCompleteLineEdit.py \
				wecase_rc.py \
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
				WConfigParser.py


Weibosdir = $(pythondir)/WeCase/weibos

Weibos_PYTHON = weibos/client.py \
				weibos/helper.py \
				weibos/__init__.py

metaconfdir = $(pythondir)/WeCase/
metaconf_DATA = WMetaConfig
