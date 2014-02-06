# HACK: only zh_CN available now

CLEANFILES = WeCase_zh_CN.qm

generate_qm = lrelease -compress -nounfinished -removeidentical

WeCase_zh_CN.qm:
	$(generate_qm) $(srcdir)/WeCase_zh_CN.ts -qm ./WeCase_zh_CN.qm

langdir = $(localedir)/WeCase
lang_DATA = WeCase_zh_CN.qm
