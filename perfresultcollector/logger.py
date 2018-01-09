import logging
import ConfigParser


class Logger(object):
    def __init__(self, name_of_file=""):
        self.path_to_conf_file = "../logger.conf"
        self.path_to_log_file = "../logger_out.log"
        self.name = name_of_file
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.path_to_conf_file)
        log_level = self.config.get("Defaults", "logging_level")
        logging.basicConfig(filename='../logger_out.log',
                            level=getattr(logging, str(log_level)))
        self.LOGGER = logging.getLogger(name_of_file)

    def set_logger_level(self, level=""):
        self.config.read(self.path_to_log_file)
        self.config.set("logging_level", level)

    def get_logger_level(self):
        self.config.read(self.path_to_conf_file)
        return self.config.get("Defaults", "logging_level")

    def debug(self, text):
        self.LOGGER.debug(text)

    def info(self, text):
        self.LOGGER.info(text)

    def warning(self, text):
        self.LOGGER.warning(text)


loger = Logger(__name__)
loger.debug("texit")
