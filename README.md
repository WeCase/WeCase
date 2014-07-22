[WeCase](http://wecase.org)
======

![WeCase](https://raw.githubusercontent.com/WeCase/WeCase/master/res/wecase.png)


A Sina Weibo Client Focusing on Linux.
---------------------------------------
The goal of WeCase, is becoming a simple, but not crude Sina Weibo client.

This project is under heavy development, we are far away from the goal now.

Installation
------------

### Installing by Package Manager

#### Arch Linux

```
yaourt -S wecase
```

#### Fedora (18, 19 only)

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

#### Dependencies
-----
1. Python 3
2. [rpweibo](https://github.com/WeCase/rpweibo)
2. PyQt4 (python3-pyqt, python3-qt4)
3. Python-notify2 (aka. python3-notify2, optional dependency)
4. Development tools for PyQt / Qt (packages names are very different on different distributions)
5. make
6. automake

Note: Some distributions use different packages names, or do not contain `python-notify2` in thier packages repositories. We are going to create `.rpm` and `.deb` packages for the dependencies. Before that, please download and install them from PIP.

#### Build and Install from Source

##### Install rpweibo

See [rpweibo](https://github.com/WeCase/rpweibo)

##### Build

```
git clone git://github.com/WeCase/WeCase.git

# Build and Install
./bootstrap.sh
mkdir build
cd build
../configure
make
sudo make install

# Run
wecase
```

Contact & Discuss
---------

### IRC Channel

[#wecase](https://kiwiirc.com/client/irc.freenode.net/wecase) @ Freenode

### Mailing List

To join the mailing list, click [here](https://groups.google.com/forum/?hl=zh-CN&fromgroups#!forum/wecase),
or send an empty mail to **wecase+subscribe@googlegroups.com**.

Development Guide
------
Everyone should follow the [Development Guide](https://github.com/WeCase/WeCase/wiki/WeCase-%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97). Please read it carefully.

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/WeCase/wecase/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
