all:
	python3 make.py
interface:
	python3 make.py ui
translate:
	python3 make.py translate
clean:
	rm -rf *_ui.py *_rc.py 2> /dev/null
lines:
	find ./ | grep ".py$$" | egrep -v "rc" | xargs wc -l
lines-noui:
	find ./ | grep ".py$$" | egrep -v "rc|ui" | xargs wc -l
