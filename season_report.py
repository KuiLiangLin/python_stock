import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def financial_statement(year, season, type='綜合損益彙總表'):
    if year >= 1000:
        year -= 1911
        
    if type == '綜合損益彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif type == '資產負債彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif type == '營益分析彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')
    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':'103',
        'season':'01',
    })
    
    r.encoding = 'utf8'
    dfs = pd.read_html(r.text)
    
    
    for i, df in enumerate(dfs):
        df.columns = df.iloc[0]
        dfs[i] = df.iloc[1:]
        
    df = pd.concat(dfs).applymap(lambda x: x if x != '--' else np.nan)
    df = df[df['公司代號'] != '公司代號']
    df = df[~df['公司代號'].isnull()]
    return df


df = financial_statement(107, 2, '營益分析彙總表')

df = df.drop(['合計：共 808 家'], axis=1)
df = df.set_index(['公司名稱'])
df = df.astype(float)

df['毛利率(%)(營業毛利)/(營業收入)'].hist(bins=range(-100,100))
df.loc['台積電']
df.loc[['台積電', '聯發科']]

#數值分析
#df.discribe()

plt.show()
df['毛利率(%)(營業毛利)/(營業收入)'].hist(bins=range(-100,100))

cond1 = df['毛利率(%)(營業毛利)/(營業收入)'].astype(float) > 20
cond2 = df['營業利益率(%)(營業利益)/(營業收入)'].astype(float) > 5
df[cond1 & cond2]
print(df)
