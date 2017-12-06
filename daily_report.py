import sys
import requests
from io import StringIO
import pandas as pd
import time

year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]


print (' -Request csv:', year, month, day, time.strftime("...... %H:%M:%S"))
url = 'http://app.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
payload = ({'download': 'csv',
            'qdate':str(year)+'/'+str(month)+'/'+str(day),#'106/10/24',
            'selectType':'ALL',})
#filename = 'daily_'+str(year)+str(month)+str(day)+'.txt'
filename = str(year)+str(month)+str(day)+'.txt'
try:
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
    df = df.drop(['漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價',
    '最後揭示賣量','開盤價','最高價','最低價','成交金額','成交筆數'], axis=1)
    print(' -Write to file:', filename)
    #del df['最後揭示買量']
    df.to_csv( './daily_report_data/'+filename, sep = '\t', encoding = 'utf8', index = False)

except BaseException:
    print(" -No Data")

#else:
#    print(" -Get Data")
    
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
