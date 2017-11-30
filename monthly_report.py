import sys
import requests
from io import StringIO
import pandas as pd
import time
    
year = sys.argv[1]
month = sys.argv[2]

print (' -Read html:', year, month, sep = ' ', end = '\n')
# 下載該年月的網站，並用pandas轉換成 dataframe
html_df = pd.read_html('http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html')

filename = 'monthly_'+str(year)+str(month)+'.txt'

try:
    dfs = []
    for i in html_df:
        try:
            dfs.append(i[list(range(0,10))])
        except:
            print('**WARRN: cannot process DataFrame:\n')
    df = pd.concat(dfs)

    '''
    # 將每一張 dataframe 做整理
    def clean_df(df):
        df = df.copy()
        df = df.drop([0,1], axis=0, errors=False)
        df = df[list(range(0,10))]
        return df


    # 將 dataframe 一一做整理
    dfs = []
    for i, df in enumerate(html_df):
        try:
            dfs.append(clean_df(df))
        except:
            print('**WARRN: cannot process DataFrame:\n', df)

    # 將所有的 dataframe 合併
    df = pd.concat(dfs)
    '''
    # 再刪除一些冗於的row
    df = df.set_index(0).drop(['合計','公司代號'], axis=0)
    df = df[~df.index.isnull()]

    # dataframe每一個column命名
    df.columns = dfs[0].loc[3][1:]

    print(' -Write to file:', filename)
    df.to_csv( filename, sep = '\t', encoding = 'utf8', index = True)
except BaseException:
    print(" -No Data")

