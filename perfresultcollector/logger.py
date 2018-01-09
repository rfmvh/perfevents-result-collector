import logging
import ConfigParser


class Logger(object):
    def __init__(self, name_of_file=""):
        self.path_to_conf_file = "../logger.conf"
        self.path_to_log_file = "../logger_out.log"
        self.name = name_of_file
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.path_to_conf_file)
        self.refresh_logger()

    def refresh_logger(self):
        log_level = self.config.get("Defaults", "logging_level")
        logging.basicConfig(filename='../logger_out.log',
                            level=getattr(logging, str(log_level.upper())))
        self.LOGGER = logging.getLogger(self.name)

    def set_logger_level(self, level=""):
        self.config.read(self.path_to_conf_file)
        self.config.set("Defaults", "logging_level", level.upper())
        with open(self.path_to_conf_file, 'wb') as configfile:
            self.config.write(configfile)

    def get_logger_level(self):
        self.config.read(self.path_to_conf_file)
        return self.config.get("Defaults", "logging_level")

    def debug(self, text):
        self.refresh_logger()
        self.LOGGER.debug(text)

    def info(self, text):
        self.refresh_logger()
        self.LOGGER.info(text)

    def warning(self, text):
        self.refresh_logger()
        self.LOGGER.warning(text)


loger = Logger(__name__)
loger.debug("texit")
loger.set_logger_level("info")
loger.debug("asdasd")
loger.warning("random")
