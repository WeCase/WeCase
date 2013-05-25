WeCase
======

Description 概述
------
The Linux Sina Weibo Client

Linux下的新浪微博客户端

This project is under heavy development.

这个项目处在开发状态。

IRC Channel IRC频道
------
\#wecase @ freenode

Development Guide 开发指南
------
Everyone should follow the [Development Guide](https://github.com/WeCase/WeCase/wiki/WeCase-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97). Please read it carefully.

所有人都应遵守[开发指南](https://github.com/WeCase/WeCase/wiki/WeCase-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97)。请务必仔细阅读

Dependencies 依赖
-----
1. Python 3 
2. PyQt4 (python3-pyqt, python3-qt4)
3. python-notify2 (python3-notify2)
4. python-requests (python3-requests)

Note: Some distributions use different packages names, or do not contain `python-notify2` in thier packages repositories. We are going to create `.rpm` and `.deb` packages for the dependencies. Before that, please download and install them from PIP.

注意：不同的发行版可能使用不同的软件包名称，或者在软件库中找不到`python-notify2`。我们将会创建这些依赖的`.rpm`以及`.deb`包，在此之前，请使用PIP安装

Installation Guide 安装指南
-----
1. Install the dependencies for WeCase. 

   安装WeCase所需要的依赖。

2. Get the source code `git clone git://github.com/WeCase/WeCase.git`

   `git clone git://github.com/WeCase/WeCase.git`得到源码

3. `cd WeCase`

4. Get the sdk `git submodule init; git submodule update`

   取得sdk`git submodule init; git submodule update`
   
5. Install SDK `cd sdk; sudo python3 setup.py install`

   安装sdk`cd sdk; sudo python3 setup.py install`
   
6. Run `python3 ./src/wecase.py` in root directory of the source code.

   在源码的根目录下运行`python3 ./src/wecase.py`
