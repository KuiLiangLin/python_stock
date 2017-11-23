
import requests
from io import StringIO
import pandas as pd


url = 'http://app.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
payload = ({'download': 'csv',
            'qdate':'106/10/24',
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

df.to_csv('0000000.txt', sep = '\t', encoding = 'utf8', index = False)
'''
f = open('01234567.txt', 'w', encoding = 'UTF-8')
for i in df.readline() :
    f.write(str(i))
    

f.close()
'''
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
