#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This model implemented a model for smileies.
# Copyright (C) 2013, 2014 The WeCase Developers.
# License: GPL v3 or later.


import path
from WeHack import Singleton
from collections import OrderedDict
try:
    from xml.etree.cElementTree import ElementTree
except ImportError:
    from xml.etree.ElementTree import ElementTree


class FaceItem():
    def __init__(self, xml_node):
        super(FaceItem, self).__init__()
        self._xml_node = xml_node

    @property
    def name(self):
        return self._xml_node.get("tip")

    @property
    def path(self):
        return path.face_path + self._xml_node[0].text

    @property
    def category(self):
        return self._xml_node[0].text.split("/")[0]


class FaceModel(metaclass=Singleton):

    def __init__(self):
        self._faces = OrderedDict()
        tree = ElementTree(file=path.face_path + "face.xml")

        category = ""
        for face in tree.iterfind("./FACEINFO/"):
            assert face.tag == "FACE"
            face = FaceItem(face)

            if category != face.category:
                category = face.category
                self._faces[category] = {}
            else:
                self._faces[category][face.name] = face

        size = tree.find("./WNDCONFIG/Align")
        self._col, self._row = int(size.get("Col")), int(size.get("Row"))

    def categories(self):
        return self._faces.keys()

    def faces_by_category(self, category):
        return iter(self._faces[category].values())

    def all_faces(self):
        for faces in self._faces.values():
            for face in faces.values():
                yield face

    def grid_size(self):
        return self._col, self._row
