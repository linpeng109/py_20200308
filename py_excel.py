import pandas as pd


def readEx(filename, sheetname):
    df = pd.read_excel(io=filename, sheet_name=sheetname)
    print('获取每列数据的类型')
    print(df.dtypes)
    print('获取数据阵列的大小，以此作为增量更新的起点')
    print(df.shape)
    print('更改列名')
    print(df)
    colNameDict = {'操作实验一栏': 'name1', 'Unnamed: 1': 'name2', 'Unnamed: 2': 'name3'}
    df.rename(columns=colNameDict, inplace=True)
    print(df)
    print('去除空值行')
    df.dropna(axis=0, how='all', inplace=True)
    print(df)
    print('去除空值列')
    df.dropna(axis=1, how='all', inplace=True)
    print(df)
    print('使用临近格填充，处理合并单元格问题')
    df.name1.fillna(method='ffill', inplace=True)  # name1列由前向后填充
    df.name2.fillna(method='ffill', inplace=True)  # name2列由前向后填充
    df.name3.fillna('0', inplace=True)
    print(df)


if __name__ == '__main__':
    readEx('d:/test1.xlsx', 0)
