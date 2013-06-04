#!/usr/bin/env python3
import sys


def fault():
    print("No filename!")
    exit()


try:
    file = sys.argv[1]
except:
    fault()
flags = ['#action', '#topic', '#idea']
undo = "#" + "undo"

events = []
for line in open(file):
    for flag in flags:
        if flag in line:
            events.append(line)
    if undo in line:
        events.pop()

for event in events:
   print(event, end="")
