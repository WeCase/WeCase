#!/usr/bin/python3
import sys


def process_import(filename, statement):
    statement = statement.replace(",", " ")
    modules = statement.split()
    for module in modules[1:]:
        print("%s -> %s" % (filename, module))

def process_from(filename, statement):
    statement = statement.replace(",", " ")
    modules = statement.split()
    main_module = modules[1]
    for module in modules[3:]:
        print("%s -> %s -> %s" % (filename, main_module, module))

for line in sys.stdin:
    line = line.replace("\n", "")
    if line.endswith(".py"):
        filename = line
    else:
        if line.startswith("import"):
            modulename = process_import(filename, line)
        elif line.startswith("from"):
            modulename = process_from(filename, line)
