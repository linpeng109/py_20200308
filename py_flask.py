from flask import Flask
from py_config import ConfigFactory
from py_logging import LoggerFactory


class MyFlask(Flask):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        super(MyFlask, self).__init__(__name__)


if __name__ == '__main__':
    config = ConfigFactory(config='py_uipath2.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()

    app = MyFlask(config=config, logger=logger)


    def callback(self, result):
        print(result)
        return result


    @app.route('/')
    def helloworld(self, event):
        logger.debug('Hello World!')
        return 'Hello World!'


    app.run(host='0.0.0.0', port=8822, debug=True)
