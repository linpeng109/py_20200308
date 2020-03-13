from multiprocessing import Pool
from multiprocessing import Process

import pandas as pd

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_path import Path
from py_qrcode import QRcode


class DataFileParser():
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config

    def __getNewFilename(self, filename, type='default'):
        newpath = self.config.get(type, 'outpath')
        Path.outpathIsExist(newpath)
        fileinfo = Path.splitFullPathFileName(filename)
        newfilename = (newpath + fileinfo.get('sep') + fileinfo.get('main') + '_OK' + '.txt')
        return newfilename

    def startProcess1(self, event):
        file = event.src_path
        try:
            if (Path.filenameIsContains(file, ['AAS.txt'])):
                process = Process(target=self.aasTxtWorker(file), args=(file,))
            if (Path.filenameIsContains(file, ['HCS', '.xls'])):
                process = Process(target=self.hcsExcelWorker(file), args=(file,))
            if (Path.filenameIsContains(file, ['HCS.txt'])):
                process = Process(target=self.hcsTxtWorker(file), args=(file,))
            if (Path.filenameIsContains(file, ['AFS', '.xlsx'])):
                process = Process(target=self.afsExcelWorker(file), args=(file,))
            if (Path.filenameIsContains(file, ['surpacToCad', 'xlsx'])):
                process = Process(target=self.surpacToCadDFWorker(file), args=(file,))
            if (Path.filenameIsContains(file, ['puid.txt'])):
                process = Process(target=self.puidWorker(file), args=(file,))
            process.start()
            # process.join(timeout=10000)
        except(ValueError):
            self.logger.error(ValueError.message)
            pass

    def startProcess2(self, event):
        file = event.src_path
        pool = Pool(10)
        try:
            if (Path.filenameIsContains(file, ['AAS.txt'])):
                results = pool.map(self.aasTxtWorker, (file,))
            if (Path.filenameIsContains(file, ['HCS', '.xls'])):
                results = pool.map(self.hcsExcelWorker, (file,))
            if (Path.filenameIsContains(file, ['HCS.txt'])):
                results = pool.map(self.hcsTxtWorker, (file,))
            if (Path.filenameIsContains(file, ['AFS', '.xlsx'])):
                results = pool.map(self.afsExcelWorker, (file,))
            if (Path.filenameIsContains(file, ['surpacToCad', 'xlsx'])):
                results = pool.map(self.surpacToCadDFWorker, (file,))
            if (Path.filenameIsContains(file, ['puid.txt'])):
                results = pool.map(self.puidWorker, (file,))
            # process.start()
            # process.join(timeout=10000)
            self.logger.debug(results[0])
        except (RuntimeError):
            self.logger.error(RuntimeError.message)
            pass

    # ========================

    def puidWorker(self, puidFilename):
        data = "http://192.168.1.104:8822/download"
        img = QRcode.getQRCode(data=data)
        img.show()

    def surpacToCadDFWorker(self, surpacToCadExcelFileName):
        # 读取
        dict = {'sheet_name': 0, 'header': None}
        surpacToCadDF = pd.read_excel(surpacToCadExcelFileName, **dict)
        self.logger.debug(surpacToCadDF)
        surpacToCadDF.drop(index=[0], inplace=True)
        return surpacToCadDF

    def hcsTxtWorker(self, hcsTextFileName):
        dict = {'sep': ' ', 'encoding': 'UTF-16', 'dtype': 'str', 'header': None, 'engine': 'python',
                'na_filter': False}
        hcsDf = pd.read_csv(filepath_or_buffer=hcsTextFileName, **dict)
        hcsDf.drop(index=[0, 1], inplace=True)
        # hcsDf.sort_index(0, ascending=False, inplace=True)
        hcsDf.dropna(axis=1, how='any', inplace=True)
        self.logger.debug(hcsDf)
        newfilename = self.__getNewFilename(filename=hcsTextFileName, type='hcs')
        self.logger.debug(newfilename)
        encoding = self.config.get('hcs', 'encoding')
        hcsDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')
        return hcsDf

    def hcsExcelWorker(self, hcsExcelFileName):
        dict = {'sheet_name': 0, 'header': None}
        hcsDf = pd.read_excel(hcsExcelFileName, **dict)
        hcsDf.drop(index=[0, 1], inplace=True)  # 删除表标题
        hcsDf.dropna(axis=1, how='any', inplace=True)
        self.logger.debug(hcsDf)
        newfilename = self.__getNewFilename(filename=hcsExcelFileName, type='hcs')
        encoding = self.config.get('hcs', 'encoding')
        hcsDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')

    def afsExcelWorker(self, afsExcelFileName):
        dict = {'sheet_name': '样品测量数据', 'header': None}
        afsDf = pd.read_excel(afsExcelFileName, **dict)
        afsDf.drop(index=[0, 1, 2], inplace=True)
        self.logger.debug(afsDf)
        newfilename = self.__getNewFilename(filename=afsExcelFileName, type='afs')
        encoding = self.config.get('afs', 'encoding')
        afsDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')

    def aasTxtWorker(self, aasTextFilename):
        dict = {'dtype': 'str',
                'header': None, 'engine': 'python'}
        aasDf = pd.read_csv(filepath_or_buffer=aasTextFilename, encoding='gbk', **dict)
        self.logger.debug(aasDf)
        newfilename = self.__getNewFilename(filename=aasTextFilename, type='aas')
        encoding = self.config.get('aas', 'encoding')
        aasDf.to_csv(newfilename, index=None, header=None, encoding=encoding, line_terminator='\r\n')
        return aasDf


if __name__ == '__main__':
    config = ConfigFactory(config='py_uipath2.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    dataFileParser = DataFileParser(config=config, logger=logger)

    # result = dataFileParser.puidWorker('e:\\uipathdir\\1212121puid.txt')
    # result = dataFileParser.surpacToCadDFWorker('e:\\uipathdir\\20200308surpacToCad.xlsx')
    result = dataFileParser.hcsTxtWorker('e:/uipathdir/20191127HCS.txt')
    print('rows=%s' % result[0].shape[0])
    print('=========')
    print('df=%s' % result)
    # print('width=%s' % result[1][1])
    # print('heigh=%s' % result[2][1])
