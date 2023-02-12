# from backtrader import cerebro
# from numpy.lib.function_base import select
import tushare as ts
# import itertools
# import numpy as np
# import matplotlib.pyplot as plt
# from tushare import stock
# from tushare.stock.trading import get_today_all
#
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# import pandas as pd
# from datetime import datetime
# import backtrader as bt
# import seaborn as sns
#
ts.set_token('ac4fb230f18cccda413f0b93cca393f2fb860865dcc3a34b72987dca')
pro = ts.pro_api()
#
#
# # 1.数据加载
# def get_data(ts_code='600519', start_date='20170101', end_date='20170201'):
#     df = ts.get_k_data(code=ts_code, start=start_date, end=end_date)
#     df.index = pd.to_datetime(df.date)
#     df['openinterest'] = 0;
#     df = df[['open', 'high', 'low', 'close', 'volum', 'oeninterest']]
#     return df
#
#
# stock_df = get_data()
# fromdate = datetime(2017, 1, 1)
# todate = datetime(2017, 2, 1)
# data = bt.feeds.PandasData(dataname=stock_df, fromdate=fromdate, todate=todate)
#
#
# # 2.构建策略
# class MyStrategy(bt.MetaStrategy):
#     params = (
#         ('maperiod,20')
#     )
#
#     def __init__(self):
#         self.order = None
#         self.ma = bt.indicators.SimpleMovingAverage(self.datas(0), period=self.params.maperiod)
#
#     def next(self):
#         if (self.order):
#             return
#         if (not self.position):
#             if self.datas[0].close[0] > self.ma[0]:
#                 self.order = self.buy(size=200)
#         else:
#             if self.datas[0].close[0] < self.ma[0]:
#                 self.order = self.sell(size=200)
#
#
# # 3.策略设置
# cerebro = bt.Cerebro()
# # 将数据加入回测系统
# cerebro.adddata(data)
# # 加入自己的策略
# cerebro.addstrategy(MyStrategy)
# # 经纪人
# startcash = 100000
# cerebro.broker.setcash(startcash)
# # 设置手续费
# cerebro.broker.setcommission(0.0002)
# # 4.执行回测
# s = fromdate.strftime("%Y-%m-%d")
# t = todate.strftime("%Y-%m-%d")
# print(f'初始资金：{startcash}\回测时间: {s}  {t}')
# cerebro.run()
# portval = cerebro.broker.getvalue()
# print(f'剩余资金：{startcash}\回测时间: {s}  {t}')

# 改版
# from numpy.lib.function_base import select
# import tushare as ts
# import itertools
# import numpy as np
# import matplotlib.pyplot as plt
# from tushare import stock
# from tushare.stock.trading import get_today_all
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# import pandas as pd
# from datetime import datetime
# import backtrader as bt
# import seaborn as sns
# 先引入后面可能用到的包（package）
import pandas as pd
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt
#% matplotlib inline

# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']

ts.set_token('ac4fb230f18cccda413f0b93cca393f2fb860865dcc3a34b72987dca')
pro = ts.pro_api()


# 1.数据加载
def get_data(ts_code='000001.SZ', start='20100101', end='20200331'):
    df = pro.daily(ts_code=ts_code, start_date=start, end_date=end)
    df = df.sort_values(by='trade_date')
    df.index = pd.to_datetime(df.trade_date)
    df['openinterest'] = 0
    df['volume'] = df['vol']
    df = df[['open', 'high', 'low', 'close', 'vol', 'openinterest']]
    return df


stock_df = get_data()


# fromdate = datetime(2015,1,1)
# todate = datetime(2022,2,1)
# data = bt.feeds.PandasData(dataname=stock_df,fromdate=fromdate,todate=todate)
# print(data)
# 2.构建策略
class MyStrategy(bt.Strategy):
    params = (
        ('maperiod', 20),
    )

    def __init__(self):
        # 指定价格序列
        self.dataclose = self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)

    def next(self):
        if (self.order):
            return
        if (not self.position):
            if self.dataclose[0] > self.sma[0]:
                self.order = self.buy(size=200)
        else:
            if self.dataclose[0] < self.sma[0]:
                self.order = self.sell(size=200)


# 3.策略设置
cerebro = bt.Cerebro()
# 将数据加入回测系统
start = datetime(2010, 3, 31)
end = datetime(2020, 3, 31)
data = bt.feeds.PandasData(dataname=stock_df, fromdate=start, todate=end)
cerebro.adddata(data)
# 加入自己的策略
cerebro.addstrategy(MyStrategy)
# 经纪人
startcash = 1000000.0
cerebro.broker.setcash(startcash)
# 设置手续费
cerebro.broker.setcommission(0.0002)
# 4.执行回测
# s = fromdate.strftime("%Y-%m-%d")
# t = todate.strftime("%Y-%m-%d")
# print(f'初始资金：{startcash}\回测时间: {s}  {t}')
cerebro.run()
d1=start.strftime('%Y%m%d')
d2=end.strftime('%Y%m%d')
print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')
#运行回测系统
cerebro.run()
#获取回测结束后的总资金
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
#打印结果
#print(f'总资金: {round(portvalue,2)}')
portval = cerebro.broker.getvalue()
#print(f'剩余资金：{startcash}\回测时间:')
cerebro.plot(volume=False)