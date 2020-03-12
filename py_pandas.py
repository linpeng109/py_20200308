import pandas as pd
from py_config import ConfigFactory
from py_logging import LoggerFactory

from multiprocessing import Pipe, Process, Pool
import winsound


class ExcelParser():
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config

    def worker(self, surpacToCadExcelFileName):
        # 读取
        dict = {'sheet_name': 0, 'header': None}
        surpacToCadDF = pd.read_excel(surpacToCadExcelFileName, **dict)
        self.logger.debug(surpacToCadDF)
        surpacToCadDF.drop(index=[0], inplace=True)
        return surpacToCadDF

    def parser(self, surpacToExcelFileName):
        pool = Pool(10)
        results = pool.map(self.worker, (surpacToExcelFileName,))
        return results[0]


if __name__ == '__main__':
    config = ConfigFactory(config='py_uipath2.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    excelParser = ExcelParser(config=config, logger=logger)

    result = excelParser.parser('e:\\uipathdir\\surpacToCad20200309.xlsx')

    print('rows=%s' % result[0].shape[0])
    print('=========')
    print('filename=%s' % result[0][1])
    print('width=%s' % result[1][1])
    print('heigh=%s' % result[2][1])
