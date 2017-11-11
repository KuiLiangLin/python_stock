
import requests
from io import StringIO
import pandas as pd

r = requests.post('http://app.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php', data={
    'download': 'csv',
    'qdate':'106/10/24',
    'selectType':'ALL',
})
r.encoding = 'big5'
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                     for i in r.text.split('\n') 
                                     if len(i.split('",')) == 16 and i[0] != '='])), header=0)


print( df[df['本益比']<15] )
