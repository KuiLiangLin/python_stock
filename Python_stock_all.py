
import requests
from io import StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#############################



#############################
def daily_report(year, month, day, filename):
    url = 'http://app.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
    payload = ({'download': 'csv',
                'qdate':str(year)+'/'+str(month)+'/'+str(day),#'106/10/24',
                'selectType':'ALL',})
    r = requests.post(url, data = payload)


    '''
    r = requests.post('http://app.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php', data={
        'download': 'csv',
        'qdate':'106/10/24',
        'selectType':'ALL',
    })
    '''

    r.encoding = 'big5'
    #r.encoding = 'utf-8'
    '''
    for i in r.text.split('\n') :
        if len(i.split('",')) == 16 and i[0] != '=' :
            print (StringIO("\n".join(i.translate({ord(c): None for c in ' '}))))
    '''


    df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                         for i in r.text.split('\n') 
                                         if len(i.split('",')) == 16 and i[0] != '='])),
                     header=0)
    #print(df.describe())
    #print (df)
    #df.columns = df[0].loc[3][1:]
    df = df.drop(['漲跌(+/-)','漲跌價差','最後揭示買價',
                               '最後揭示買量','最後揭示賣價','最後揭示賣量'], axis=1)
    #del df['最後揭示買量']
    df.to_csv( filename, sep = '\t', encoding = 'utf8', index = False)
    return df
'''
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                     for i in r.text.split('\n') 
                                     if len(i.split('",')) == 16 and i[0] != '='])), header=0)


print( df[df['本益比']<15] )

input()
'''

'''
print()
r = 'we fgh ra'
transtable = {ord(c): None for c in 'ef'}
print (transtable)
print()
print()
strp = r.translate(transtable)
print (strp)
'''
#############################



#############################
def monthly_report(year, month):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    html_df = pd.read_html('http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html')


    
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
    
    # 再刪除一些冗於的row
    df = df.set_index(0).drop(['合計','公司代號'], axis=0)
    df = df[~df.index.isnull()]
    
    # dataframe每一個column命名
    df.columns = dfs[0].loc[3][1:]
    return df



#############################



#############################

def financial_statement(year, season, table):#='綜合損益彙總表'):
    if year >= 1000:
        year -= 1911
        
    if table == 1:#'綜合損益彙總表':
        #url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
        url = 'http://mops.twse.com.tw/mops/web/t163sb04'
    elif table == 2:# '資產負債彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif table == 3:#'營益分析彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')
        

    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':'106',
        'season':'01',
    })
    
    r.encoding = 'utf8'
    dfs = pd.read_html(r.text)
    
    '''
    for i, df in enumerate(dfs):
        df.columns = df.iloc[0]
        dfs[i] = df.iloc[1:]
        
    df = pd.concat(dfs).applymap(lambda x: x if x != '--' else np.nan)
    df = df[df['公司代號'] != '公司代號']
    df = df[~df['公司代號'].isnull()]
    
    return df
    '''


   


    return dfs

#df = financial_statement(107, 3, '營益分析彙總表')
    #df = df.drop(['合計：共 808 家'], axis=1)
    #df = df.set_index(['公司名稱'])
    #df = df.astype(float)
'''
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
'''
#print(df)

#############################



#############################
'''
data = pd.read_csv('data.csv', index_col='Unnamed: 0')


#process data
#我們將資料分成三類，一類是跑回測用的dbacktest，另一類是機器學習用的dtraning，另外一個是traning完用來評估的dtest。
from sklearn.model_selection import train_test_split
# clear data 將爛資料去掉
data.dropna(how='any', inplace=True)
# 選擇2015年以後的資料作為回測用
dbacktest = data[data['buy_date'] > '2015']
# 將其於的資料再分成兩類：dtrain 跟 dtest
dataTrainTest = data[data['sell_date'] < '2015']
dtrain, dtest = train_test_split(dataTrainTest, test_size=0.10, random_state=42)
# 設定我們的feature要用哪些
features = data.columns[5:-1]





#learning
#這邊我們用很簡單的隨機森林，來完成的，可以參考連結來學習怎麼樣調整參數，這應該算是機器學習中，前製作業最少的模型了！
from sklearn.ensemble import RandomForestClassifier
# 創建機器學習的model
rf = RandomForestClassifier(n_estimators=10, criterion='gini', 
                            max_depth=None, min_samples_split=2, 
                            min_samples_leaf=1, min_weight_fraction_leaf=0.0, 
                            max_features='auto', max_leaf_nodes=None, 
                            bootstrap=True, oob_score=False, n_jobs=1, 
                            random_state=None, verbose=0, warm_start=False, 
                            class_weight=None)
# 分類能 獲利 > 10％ 的股票
rf.fit(dtrain[features], dtrain['獲利'] > 1)






#predict
result = rf.predict(dtest[features])
print('test data')
print('gain before filtered', dtest['獲利'].mean())
print('gain after filtered', dtest['獲利'][result].mean())
print('num stocks', sum(result), '/', len(dtest))
result = rf.predict(dbacktest[features])
print('backtest data')
print('gain before filtered', dbacktest['獲利'].mean())
print('gain after filtered', dbacktest['獲利'][result].mean())
print('num stocks', sum(result), '/', len(dbacktest))





#backtest
plt.show()
dbacktest['預測'] = pd.Series(result, index=dbacktest.index)
dates = list(set(dbacktest['buy_date']))
dates.sort()
history = []
for d in dates:
    history.append(dbacktest[(dbacktest['buy_date'] == d) & (dbacktest['預測'])]['獲利'].mean())
    
pd.Series(history, index=dates).cumprod().plot()
'''


#############################



#############################



#############################
'''
f = open('檔案', '模式')

r - 讀取(檔案需存在)
w - 新建檔案寫入(檔案可不存在，若存在則清空)
a - 資料附加到舊檔案後面(游標指在EOF)
r+ - 讀取舊資料並寫入(檔案需存在且游標指在開頭)
w+ - 清空檔案內容，新寫入的東西可在讀出(檔案可不存在，會自行新增)
a+ - 資料附加到舊檔案後面(游標指在EOF)，可讀取資料
b - 二進位模式
'''

#############################


#print (daily_report(106,10,24))
daily_report(106, 10, 24, '122345.txt')
print('Done')

# 民國100年1月
#print(monthly_report(105,1))

# 西元2011年1月
#print(monthly_report(106,10))




#print(financial_statement(107, 3, 1).drop(['合計：共 809 家'], axis=1).set_index(['公司名稱']).astype(float))
#f.write(print(financial_statement(107, 1, 1)))
#print(f.read())





