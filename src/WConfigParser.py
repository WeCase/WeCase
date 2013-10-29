#!/usr/bin/env python3
from sys import stderr
from copy import deepcopy
from configparser import ConfigParser


class WConfigParser():

    ITEM = {
        "section": "", "type": None,
        "name": "", "default": None
    }

    def __init__(self, schema, config, section=""):
        self._section = section
        self._config_path = config
        self._options = []
        self._config = ConfigParser()
        self._config.read(config)
        self.__parse__(schema)

    def __parse__(self, schema):
        schema = open(schema)

        config_item = deepcopy(self.ITEM)
        for line in schema:
            if line.strip() == "":
                if config_item:
                    self._options.append(config_item)
                    config_item = deepcopy(self.ITEM)
                continue

            name, value = line.replace("\n", "").replace(" ", "").split("=")
            try:
                config_item[name] = value
            except KeyError:
                print("Invaild line: %s" % line, file=stderr)
        schema.close()

    def _get_option(self, name):
        for i in self._options:
            if i["name"] == name:
                return i

    def __getattr__(self, attr):
        option = self._get_option(attr)
        if not option:
            raise AttributeError

        try:
            return eval("%s(%s)" % (option["type"], self._config[self._section][attr]))
        except (KeyError, TypeError):
            return eval("%s(%s)" % (option["type"], option["default"]))

    def save(self):
        # TODO: Create and check the lock file during writing
        with open(self._config_path, "w+") as config_file:
            self._config.write(config_file)
