#!/usr/bin/env python3
from sys import stderr
from copy import deepcopy
from configparser import ConfigParser


class WConfigParser():

    ITEM = {
        "section": "", "type": None,
        "name": "", "alias": "",
        "default": None
    }

    def __init__(self, schema, config, section=""):
        self._section = section
        self._config_path = config
        self._options = []
        self._config = ConfigParser()
        self._config.read(config)
        self.__parse__(schema)
        self.__setattr__impl = self.__setattr__postload

    def __parse__(self, schema):
        with open(schema) as schema_file:
            schema = schema_file.readlines()

        config_item = deepcopy(self.ITEM)

        lineno = 0
        for line in schema:
            lineno += 1
            if line.strip() == "":
                if config_item:
                    self._options.append(config_item)
                    config_item = deepcopy(self.ITEM)
                continue

            name, value = line.replace("\n", "").split("=")
            name = name.strip()
            value = value.strip()

            try:
                config_item[name] = value
            except KeyError:
                print("Invaild line: %s" % line, file=stderr)

            if lineno == len(schema):
                if config_item:
                    self._options.append(config_item)
                    config_item = deepcopy(self.ITEM)
                continue

    def _get_option(self, name):
        for i in self._options:
            if i["name"] == name or i["alias"] == name:
                return i

    def __setattr__preload(self, attr, value):
        super(WConfigParser, self).__setattr__(attr, value)

    def __setattr__postload(self, attr, value):
        if not self._config.has_section(self._section):
            self._config[self._section] = {}
        try:
            # convert alias to realname
            option = self._get_option(attr)
            attr = option["name"]
        except Exception as e:
            print(e)
            pass
        self._config[self._section][attr] = str(value)

    __setattr__impl = __setattr__preload

    def __setattr__(self, attr, value):
        self.__setattr__impl(attr, value)

    def __getattr__(self, attr):
        option = self._get_option(attr)
        attr = option["name"]  # convert alias to realname

        if not option:
            raise AttributeError("WConfigParser object has no attribute '%s'" % attr)

        type = eval(option["type"])
        try:
            value = self._config[self._section][attr]
        except KeyError:
            value = option["default"]

        if type is str:
            return value
        else:
            return type(eval(value))

    def save(self):
        # TODO: Create and check the lock file during writing
        with open(self._config_path, "w+") as config_file:
            config_file.seek(0)
            config_file.write("# WeCase Configuration File, by WeCase Project.\n")
            config_file.write("# DO NOT EDIT ON NORMAL PURPOSE.\n\n")
            self._config.write(config_file)
