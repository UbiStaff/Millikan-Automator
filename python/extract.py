#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 22:31:01 2018

@author: ricktjwong
"""

import matplotlib as mpl
import numpy as np
import pandas as pd
import pims
import trackpy as tp
from slicerator import pipeline  # or: from pims import pipeline

# 定义一个灰度转换函数，将彩色帧转换为灰度图像
@pipeline
def as_grey(frame):
    red = frame[:, :, 0]  # 提取红色通道
    green = frame[:, :, 1]  # 提取绿色通道
    blue = frame[:, :, 2]  # 提取蓝色通道
    # 使用加权平均法计算灰度值
    return 0.2125 * red + 0.7154 * green + 0.0721 * blue

# 设置 matplotlib 的默认参数
mpl.rc('figure',  figsize=(10, 6))  # 设置图像大小
mpl.rc('image', cmap='gray')  # 设置图像颜色映射为灰度

def compute_traj(filename):
    # 读取视频文件
    vid = pims.Video('/Users/huzihao/Desktop/millikan-master/test_video/' + filename)
    # 将视频帧转换为灰度图像
    # 将视频帧转换为灰度图像并强制展开为列表，避免并发迭代冲突
    frames = list(as_grey(vid))
    #frames = as_grey(vid)

    # 计算视频的中点帧，并选择中点前后各 60 帧的范围
    midpoint = len(frames) / 2
    start = int(midpoint - 60)  # 起始帧(默认60)
    stop = int(midpoint + 60)  # 结束帧(默认60)

    # 使用 trackpy 批量处理帧，识别油滴
    # 参数说明：
    # - frames[start:stop]: 处理的帧范围
    # - 11: 油滴的直径（以像素为单位），可以根据实际情况调整（diameter）
    # - invert=False: 不反转图像
    # - minmass=160: 油滴的最小质量阈值，低于此值的点会被忽略，可以根据实际情况调整
    # - maxsize=3.0: 油滴的最大尺寸阈值，超过此值的点会被忽略，可以根据实际情况调整
    # - engine="numba": 使用 numba 加速计算
    f = tp.batch(frames[start:stop], 11, invert=False, minmass=160, maxsize=3.0, engine="numba")

    # 将识别到的油滴在不同帧之间进行链接，形成轨迹
    # 参数说明：
    # - f: 识别到的油滴数据
    # - 5: 最大链接距离（以像素为单位），可以根据实际情况调整
    # - memory=3: 允许油滴在 3 帧内消失后重新出现，可以根据实际情况调整
    t = tp.link_df(f, 5, memory=3)

    # 过滤掉轨迹长度小于 60 帧的油滴
    t1 = tp.filter_stubs(t, 60)

    # 打印过滤前后的油滴数量
    print('Before:', t['particle'].nunique())  # 过滤前的油滴数量
    print('After:', t1['particle'].nunique())  # 过滤后的油滴数量

    # 提取油滴的运动数据
    data = []
    for item in set(t1.particle):
        sub = t1[t1.particle == item]  # 提取单个油滴的轨迹数据
        dvx = np.diff(sub.x)  # 计算 x 方向的速度变化
        dvy = np.diff(sub.y)  # 计算 y 方向的速度变化
        for x, y, dx, dy, frame, mass, size, ecc, signal, raw_mass, ep in \
        zip(sub.x[:-1], sub.y[:-1], dvx, dvy, sub.frame[:-1], sub.mass[:-1], sub['size'][:-1], sub.ecc[:-1], sub.signal[:-1], sub.raw_mass[:-1], sub.ep[:-1]):
            # 将油滴的运动数据保存到列表中
            data.append({
                'dx': dx,  # x 方向的速度变化
                'dy': dy,  # y 方向的速度变化
                'x': x,  # x 坐标
                'y': y,  # y 坐标
                'frame': frame,  # 帧编号
                'particle': item,  # 油滴编号
                'size': size,  # 油滴尺寸
                'ecc': ecc,  # 油滴的偏心率
                'signal': signal,  # 信号强度
                'mass': mass,  # 油滴质量
                'raw_mass': raw_mass,  # 原始质量
                'ep': ep  # 其他参数
            })
    # 将数据转换为 DataFrame
    df = pd.DataFrame(data)
    # 将数据保存到 CSV 文件
    df.to_csv('/Users/huzihao/Desktop/millikan-master/csvs/extract.csv')

if __name__ == '__main__':
    # 调用 compute_traj 函数处理视频文件
    compute_traj("test-vid.MOV")