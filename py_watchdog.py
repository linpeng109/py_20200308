import multiprocessing
import time
import os
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver as Observer

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_pandas import ExcelParser
from py_tkinter import AppUI


class WatchDogObServer():

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.excelParser = ExcelParser(config=config, logger=logger)

    def on_modified(self, event):
        self.logger.debug(event)
        result = self.excelParser.parser(event.src_path)
        AppUI(result)
        self.logger.debug(result)

    def on_created(self, event):
        self.logger.debug(event)
        result = self.excelParser.parser(event.src_path)
        # AppUI(result)
        self.logger.debug(result)

    def start(self):
        path = self.config.get('watchdog', 'path')
        patterns = self.config.get('watchdog', 'patterns').split(';')
        ignore_directories = self.config.getboolean('watchdog', 'ignore_directories')
        ignore_patterns = self.config.get('watchdog', 'ignore_patterns').split(';')
        case_sensitive = self.config.getboolean('watchdog', 'case_sensitive')
        recursive = self.config.getboolean('watchdog', 'recursive')

        event_handler = PatternMatchingEventHandler(patterns=['*'],
                                                    ignore_patterns=ignore_patterns,
                                                    ignore_directories=ignore_directories,
                                                    case_sensitive=case_sensitive)
        event_handler.on_created = self.on_created
        event_handler.on_modified = self.on_modified

        observer = Observer()
        observer.schedule(path=path, event_handler=event_handler, recursive=recursive)

        observer.start()
        self.logger.debug('WatchDog Observer is startting.....')
        self.logger.debug('patterns=%s' % patterns)
        self.logger.debug('path=%s' % path)
        try:
            while observer.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.debug('WatchDog Observer is stoped.')
        observer.join()


if __name__ == '__main__':
    if os.sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    config = ConfigFactory(config='py_uipath2.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    wObserver = WatchDogObServer(config=config, logger=logger)
    wObserver.start()
