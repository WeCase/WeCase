WeCase
======

Description 概述
------
The Linux Sina Weibo Client

Linux下的新浪微博客户端

This project is under heavy development.

这个项目处在努力开发状态。

IRC Channel IRC频道
------

###使用IRC客户端

加入irc.freenode.net的#wecase频道

###使用浏览器

点击[#wecase](https://kiwiirc.com/client/irc.freenode.net/wecase)在线加入IRC频道

订阅邮件列表
-----

发送空邮件到 **wecase+subscribe@googlegroups.com**

或者点击[这里](https://groups.google.com/forum/?hl=zh-CN&fromgroups#!forum/wecase)加入


Development Guide 开发指南
------
Everyone should follow the [Development Guide](https://github.com/WeCase/WeCase/wiki/WeCase-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97). Please read it carefully.

所有人都应遵守[开发指南](https://github.com/WeCase/WeCase/wiki/WeCase-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97)。请务必仔细阅读。

Dependencies 依赖
-----
1. Python 3 
2. PyQt4 (python3-pyqt, python3-qt4)

3. Optional 可选

   Python-notify2 (python3-notify2)

Note: Some distributions use different packages names, or do not contain `python-notify2` in thier packages repositories. We are going to create `.rpm` and `.deb` packages for the dependencies. Before that, please download and install them from PIP.

注意：不同的发行版可能使用不同的软件包名称，或者在软件库中找不到 `python-notify2`。我们将会创建这些依赖的 `.rpm` 以及 `.deb` 包，在此之前，请从 PIP 安装。

Installation Guide
-----

### Installing by Package Manager

#### Arch Linux

```
yaourt -S wecase
```

#### Fedora (18, 19)

```
sudo su -c "wget -O- http://download.opensuse.org/repositories/home:/biergaizi/Fedora_$(rpm -E %fedora)/home:biergaizi.repo > /etc/yum.repos.d/wecase.repo"
sudo yum install WeCase
```

#### Gentoo

```
layman -a gentoo-zh
emerge net-misc/WeCase
```

### Build from Source

```
git clone --recursive git://github.com/WeCase/WeCase.git

# SDK Installation
cd WeCase/sdk
sudo python3 setup.py install
cd ..

# Build and Install
mkdir build
cd build
../configure
make
sudo make install

# Run
wecase
```
