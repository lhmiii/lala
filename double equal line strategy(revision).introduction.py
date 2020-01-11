
"""
#双均线策略
本策略以沪深300指数（399300.SZ)为标的建立双均线模型，数据时间跨度为2010.12.31至2019.12.31
对数据进行对齐清洗以后，通过SMA计算得到以收盘价为基础的周期为5的短期移动平均线以及周期为60的长期移动平均线
当短期均线高于长期均线时做多，即买入股票，增加仓位
图像分别为移动平均线图，仓位图及净值曲线图

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import talib

#数据下载
pro = ts.pro_api()
data_df = pro.index_daily(ts_code='399300.SZ', start_date='20101231', end_date='20191231')

#数据对齐、清洗
data_df['trade_date'] = pd.to_datetime(data_df['trade_date'])
data_df = data_df.set_index('trade_date')
data_df = data_df.sort_index() # 排序

# 双均线实现
data_df['ma_5'] = talib.SMA(data_df['close'], timeperiod = 5)
data_df['ma_60'] = talib.SMA(data_df['close'], timeperiod = 60)

# 产生信号
data_df['position'] = np.where(data_df['ma_5'] > data_df['ma_60'], 1, 0)
data_df['position'] = data_df['position'].shift(1)

# 回测
data_df['ret'] = data_df['pct_chg'] * data_df['position']
data_df['value'] = data_df['ret'].cumsum()

##############################################################################
# 可视化、回测
fig2 = plt.figure(figsize=(50,24))
ax1 = fig2.add_subplot(311, ylabel='ma')
ax2 = fig2.add_subplot(312, ylabel='posotion')
ax3 = fig2.add_subplot(313, ylabel='value')

# 均线
ax1.plot(data_df['ma_5'],'black',label = 'ma_5')
ax1.plot(data_df['ma_60'],'g',label = 'ma_60')
# 仓位
ax2.plot(data_df['position']) 
ax2.set_ylim(-0.1, 1.1)

# 净值曲线
ax3.plot(data_df['value'])

