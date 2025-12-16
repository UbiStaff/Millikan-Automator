#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modified version of transform.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import trackpy as tp
import os

# 确保 CSV 目录路径正确，设置输入和输出路径
csv_path = os.path.join(os.path.dirname(__file__), '../csvs/extract.csv')  # 输入文件路径（包含粒子轨迹数据）
output_path = os.path.join(os.path.dirname(__file__), '../csvs/transformed.csv')  # 输出文件路径（计算后的数据）

# 检查文件是否存在，如果没有找到文件，则抛出异常
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Error: '{csv_path}' not found. Make sure extract.py ran successfully.")

# 读取提取的粒子轨迹数据
df = pd.read_csv(csv_path)

# 计算漂移并绘制漂移图
x = tp.compute_drift(df)  # 计算粒子的漂移
x.plot()  # 绘制漂移图
plt.show()  # 显示漂移图

# 轨迹绘制函数，绘制粒子i的轨迹
def plotTraj(i):
    particle = df.loc[df['particle'] == i]  # 获取粒子i的数据
    plt.plot(particle['frame'], particle['x'])  # 绘制粒子i在x轴上的位置变化
    turning_index = particle['y'].idxmax()  # 找到y坐标最大值的索引，即转向点
    bef = particle[:turning_index]  # 获取转向点之前的轨迹
    aft = particle[turning_index:]  # 获取转向点之后的轨迹
    return bef, aft

# 过滤粒子，根据转向点靠近中间点的粒子进行筛选
def returnParticles(middle):
    filtered, turning_indices = [], []  # 初始化筛选结果
    for i in pivoted_y:  # 遍历每个粒子
        turning_index = pivoted_y[i].idxmax()  # 获取粒子的转向点
        if abs(turning_index - middle) < 1000:  # 判断转向点是否在指定范围内（<10）                  #############
            filtered.append(i)  # 如果在范围内，添加到过滤粒子列表
            turning_indices.append(turning_index)  # 记录转向点的索引
    return filtered, turning_indices  # 返回筛选后的粒子和转向点索引

# 计算平均转向点的位置，得到整体的转向趋势
def filterParticles():
    turning_indices = [pivoted_y[i].idxmax() for i in pivoted_y]  # 获取每个粒子的转向点
    return int(sum(turning_indices) / len(turning_indices))  # 计算转向点的平均位置并返回

# 根据转向点计算最终的数据
def returnFinal(voltage):
    final = []  # 存储最终结果
    for i, j in zip(filtered_particles, turning_indices):  # 遍历过滤后的粒子和对应的转向点
        particle = pivoted_dy[i].dropna()  # 获取粒子的y方向速度（去除缺失值）
        size = pivoted_size[i].dropna()  # 获取粒子的大小
        ecc = pivoted_ecc[i].dropna()  # 获取粒子的偏心率
        signal = pivoted_signal[i].dropna()  # 获取粒子的信号强度
        mass = pivoted_mass[i].dropna()  # 获取粒子的质量
        ep = pivoted_ep[i].dropna()  # 获取粒子的ep参数

        bef = particle[:j - particle.index[0]]  # 获取转向点之前的粒子数据
        aft = particle[j - particle.index[0]:]  # 获取转向点之后的粒子数据

        if len(bef) > 0 and len(aft) > 0:  # 确保前后都有数据
            # 计算转向前的平均速度（v_e）和转向后的平均速度（v_g）
            v_e = bef.sum() / len(bef)
            v_g = aft.sum() / len(aft)
            # 根据速度计算静电学中涉及的量
            ve_si = v_e * 30 / 8 * 0.05E-03  # 计算v_e对应的速度，单位转换
            vg_si = v_g * 30 / 8 * 0.05E-03  # 计算v_g对应的速度，单位转换
            k = 3.39249E-08  # 常数k
            # 根据速度计算电荷（charge）和粒子的电荷数（n）
            charge = k * abs(vg_si)**0.5 * (abs(vg_si) + abs(ve_si)) / (voltage / 0.006)
            n = charge / 1.60217662E-19  # 计算电荷数（n）

            # 将粒子的最终数据添加到结果中
            final.append({
                'particle': i, 'turning_point': j, 'v_e': ve_si, 'v_g': vg_si,
                'n': n, 'size': size.mean(), 'ecc': ecc.mean(),
                'signal': signal.mean(), 'mass': mass.mean(), 'ep': ep.mean()
            })
    return final  # 返回最终结果

# 数据透视操作，将数据根据粒子编号进行重塑
pivoted = df.pivot(index='frame', columns='particle')  # 将数据根据帧号和粒子编号进行透视
pivoted_y = pivoted['y']  # 提取y坐标数据
pivoted_dy = pivoted['dy']  # 提取y方向速度数据
pivoted_size = pivoted['size']  # 提取粒子大小数据
pivoted_ecc = pivoted['ecc']  # 提取粒子偏心率数据
pivoted_signal = pivoted['signal']  # 提取粒子信号数据
pivoted_mass = pivoted['mass']  # 提取粒子质量数据
pivoted_ep = pivoted['ep']  # 提取粒子的ep参数

# 根据转向点的中心位置进行粒子过滤
filtered_particles, turning_indices = returnParticles(184)

# 根据指定电压计算最终结果
final = returnFinal(141)  # 电压参数可以在此修改（原始144）（144）

#附加
# 可视化每个筛选后的粒子的 y 方向轨迹
for i in filtered_particles:
    plt.plot(pivoted_y[i])
    plt.title(f"Particle {i} Y Trajectory")
    plt.xlabel("Frame")
    plt.ylabel("Y position (pixels)")
    plt.show()
#附加

# 将最终数据保存到 CSV 文件中
df_final = pd.DataFrame(final)  # 将最终数据转换为 DataFrame 格式
df_final.to_csv(output_path, index=False)  # 保存数据到文件
print(f"Data saved to {output_path}")  # 输出保存成功的信息