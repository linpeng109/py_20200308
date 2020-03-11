from configparser import ConfigParser


class ConfigFactory():
    def __init__(self, config):
        self.config = config

    class _Configparser(ConfigParser):
        def optionxform(self, optionstr):
            return optionstr

    def getConfig(self):
        cfg = self._Configparser()
        cfg.read(filenames=self.config, encoding='utf8')
        return cfg


if __name__ == '__main__':
    cfg = ConfigFactory(config='py_uipath2.ini').getConfig()
    dic = dict(cfg.items('logger'))
    print(dic)
