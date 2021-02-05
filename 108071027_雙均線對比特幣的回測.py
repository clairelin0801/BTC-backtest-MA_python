# -*- coding: utf-8 -*-
'''
Created on Sat May  2 23:59:32 2020
首先，先抓取需要的比特幣資料
讀檔
刪除不需要用到的欄位，這裡保留收盤價，把時間當成index
畫出長、短兩條週期均線
這裡取最新600天的資料來做圖

計算黃金交叉和死亡交叉
計算「短線」減去「長線」之差，asign 會在這個數大於 0 時回傳 +1，小於 0 時回傳-1
+1代表短線在長線上方，-1代表長線在短線上方
黃金交叉發生於-2，死亡交叉發生於+2
結果存到 golden_cross和 death_cross 裡面
算出有幾次黃金和死亡交叉

@author: 林羽霈
'''

import urllib.request
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

start = input("請輸入開始時間:")
end = input("請輸入結束時間:")

def getPriceData(start,end):

    start = start.split('-')
    end = end.split('-')
    
    time1=int(datetime(int(start[0]),int(start[1]),int(start[2])).timestamp()) + 86400

    time2=int(datetime(int(end[0]),int(end[1]),int(end[2])).timestamp()) + 86400
    
    url = "https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=" + str(time1) + "&period2=" + str(time2) + "&interval=1d&events=history"

    urllib.request.urlretrieve(url,'BTC.csv')

getPriceData(start,end)


df = pd.read_csv('BTC.csv') 
df.set_index(['Date'],inplace = True)
df = df[['Close']]
df = df.dropna()

short_period = input("短週期天數：")
long_period = input("長週期天數：")

df['ma_short'] = df['Close'].rolling(int(short_period)).mean()
df['ma_long'] = df['Close'].rolling(int(long_period)).mean()

df[['Close', 'ma_short', 'ma_long']][-600:-1].plot(figsize = (20, 10)) 
                                     #可以自行更改判斷區間
plt.show()


df['diff'] = df['ma_short'] - df['ma_long']
asign = np.sign(df['diff'])
cross_signal = ((np.roll(asign, 1) - asign) == (-2)).astype(int) 
# 回傳 T(1) 或 F(0)
df['golden_cross'] = cross_signal # 結果存到 golden_cross 裡面

asign = np.sign(df['diff'])
death_signal = ((np.roll(asign, 1) - asign) == 2).astype(int)
df['death_cross'] = death_signal # 結果存到 death_cross 裡面

df['death_cross'][df['death_cross'] == 1] = (-1) 
# 為了和黃金交叉有分別，把本來的 1 改成 -1

print("黃金交叉總共有 %d 次" % df['golden_cross'].sum())
print("死亡交叉總共有 %d 次" % df['death_cross'].sum())
