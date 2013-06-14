from configparser import ConfigParser

class WeCaseConfig():

    def __init__(self, path, section="main"):
        self._path = path
        self._config = ConfigParser()
        self._config.read(path)

        # create a empty field
        if not self._config.has_section(section):
            self._config[section] = {}

        self._main_config = self._config[section]

    def save(self):
        # TODO: Create and check the lock file during writing
        with open(self._path, "w+") as config_file:
            self._config.write(config_file)

    # Section: main
    @property
    def notify_interval(self):
        return int(self._main_config.get("notify_interval", "30"))

    @notify_interval.setter
    def notify_interval(self, second):
        self._main_config["notify_interval"] = str(second)

    @property
    def notify_timeout(self):
        return int(self._main_config.get("notify_timeout", "5"))

    @notify_timeout.setter
    def notify_timeout(self, second):
        self._main_config["notify_timeout"] = str(second)

    @property
    def remind_comments(self):
        return self._main_config.getboolean("remind_comments", True)

    @remind_comments.setter
    def remind_comments(self, state):
        self._main_config["remind_comments"] = str(state)

    @property
    def remind_mentions(self):
        return self._main_config.getboolean("remind_mentions", True)

    @remind_mentions.setter
    def remind_mentions(self, state):
        self._main_config["remind_mentions"] = str(state)

    @property
    def usersBlacklist(self):
        return eval(self._main_config.get("usersBlacklist", "[]"))

    @usersBlacklist.setter
    def usersBlacklist(self, users):
        self._main_config["usersBlacklist"] = str(users)

    @property
    def tweetsKeywordsBlacklist(self):
        return eval(self._main_config.get("tweetKeywordsBlacklist", "[]"))

    @tweetsKeywordsBlacklist.setter
    def tweetsKeywordsBlacklist(self, keywords):
        self._main_config["tweetKeywordsBlacklist"] = str(keywords)

    # Section: login
    @property
    def passwd(self):
        return eval(self._main_config.get("login", "{}"))

    @passwd.setter
    def passwd(self, accounts):
        self._main_config["login"] = str(accounts)

    @property
    def last_login(self):
        return str(self._main_config.get("last_login", ""))

    @last_login.setter
    def last_login(self, account):
        self._main_config["last_login"] = str(account)

    @property
    def auto_login(self):
        return self._main_config.getboolean("auto_login", False)

    @auto_login.setter
    def auto_login(self, state):
        self._main_config["auto_login"] = str(state)