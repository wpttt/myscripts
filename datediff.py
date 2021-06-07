#!/usr/bin/env python
# coding: utf-8

"""
============================================================================
DOS下或Batch脚本中此py脚本调用方式：python datediff.py 输入文件名 输出文件名
----------------------------------------------------------------------------
说明：
本脚本主要用于计算发震间隔
对以空格分隔的“年 月 日 时 分 秒 震级”格式数据进行时间间隔计算，
并将结果输出至GMT绘图可用的文本文件：timediff.dat
----------------------------------------------------------------------------
输入数据格式： 年 月 日 是 分 秒 震级
输出数据格式： GMT时间 天数差 小时差 震级

GMT时间格式：年-月-日T时:分:秒
============================================================================
"""

import sys
import time
import datetime
import pandas as pd


## 设置变量的接收方式，为python datediff.py 输入文件名
infile = sys.argv[1]
outfile = sys.argv[2]

timenow = datetime.datetime.now()
dftmp = pd.DataFrame({'datetime':[timenow],'mag':[0.0]})

## 读取传入文件为DataFrame
df = pd.read_csv(infile, sep=' ',names=['year','month','day','hour','minute','second','magnitude'])
print('Read data below：\n',df.head())   # 打印读取结果

## 将分列的时间数据转为时间格式
df2 = pd.DataFrame(pd.to_datetime(df[['year','month','day','hour','minute','second']]),columns=['datetime'])
df2['mag'] = df['magnitude']
df22 = df2.append(dftmp, ignore_index=True)
df22['datetime2'] = df22['datetime'].shift()  # 新建时间列，将其设置为上一行的时间值

## 时间列相减，得到时间差，并将时间差转为天数，保留两位小数
df22['daydiff'] = df22.apply(
    lambda x: round((x.datetime - x.datetime2).days + 
    (x.datetime - x.datetime2).seconds/3600/24,2),
    axis=1
)
df22['hourdiff'] = df22.apply(
    lambda x: round((x.datetime - x.datetime2).days*24 + 
    (x.datetime - x.datetime2).seconds/3600,2),
    axis=1
)

## 将时间转为GMT时间格式
df22['Time'] = df22.apply(
    lambda x: str(x.datetime).split(' ')[0] + 'T' + 
    str(x.datetime).split(' ')[1], axis=1
)
# print('Transformed data to below format：\n',df2.head())  # 打印计算和转换结果

## 提取时间、天数差、小时差、震级列至df3，并保存为文本文件timediff.dat
df3 = df22[['Time','daydiff','hourdiff','mag']]
df3 = df3.where(df3.notnull(), 0)
print('Result data：\n',df3.head())   #保存前打印结果

df3.to_csv(outfile, sep=' ', header=False, index=False) # 保存数据
print('Done')
