#!/usr/bin/env python3
import sys
import os
UI_PATH = "./ui"


def is_ui(filename):
    if filename.split('.')[-1] == "ui":
        return True
    else:
        return False


def is_rc(filename):
    if filename.split('.')[-1] == "qrc":
        return True
    else:
        return False


def generate_ui(name, path):
    print("Generating UI file for %s" % (file))
    os.popen("pyuic4 %s > %s.py" % (path, file.replace('.ui', '_ui')))


def generate_rc(name, path):
    print("Generating RC file for %s" % (file))
    os.popen("pyrcc4 -py3 -compress 9 %s > %s.py" % (path, file.replace(".qrc", "_rc")))


def process_ui():
    global file
    for file in os.listdir(UI_PATH):
        path = os.path.join(UI_PATH, file)
        if os.path.isdir(path):
            continue

        if is_ui(file):
            generate_ui(file, path)

        if is_rc(file):
            generate_rc(file, path)


def process_translate():
    os.system("pylupdate4 wecase.pro")
    os.system("lrelease wecase.pro")


if len(sys.argv) < 2:
    process_ui()
    process_translate()
elif sys.argv[1] == "ui":
    process_ui()
elif sys.argv[1] == "translate":
    process_translate()
