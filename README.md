WeCase
======

Description
------
The Linux Sina Weibo Client

This project is under heavy development.

**特别说明：在使用 l10n 框架之前，严禁任何人以任何理由翻译界面！**

**WARNING: Nobody is allowed to translate the UI until we use l10n framework!!**

IRC Channel
------
\#wecase @ freenode

Development Guide
------
Everyone should follow the [Development Guide](https://github.com/WeCase/WeCase/wiki/WeCase-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97). Please read it carefully.

Dependencies
-----
1. Python 3 
2. PyQt4 (python3-pyqt, python3-qt4)
3. python-notify2 (python3-notify2)
4. python-requests (python3-requests)

Note: Some distributions use different packages names, or do not contain `python-notify2` in thier packages repositories. We are going to create `.rpm` and `.deb` packages for the dependencies. Before that, please download and install them from PIP.

Installation Guide
-----
1. Install the dependencies for WeCase.
2. Get the source code `git clone git://github.com/WeCase/WeCase.git`
3. `cd WeCase`
4. Get the sdk `git submodule init; git submodule update`
5. Install SDK `cd sdk; sudo python3 setup.py install`
6. Run `python3 ./src/wecase.py` in root directory of the source code.
