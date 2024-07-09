import random
import numpy as np
from utils import log_dict_to_file


def paramGen():
    param_dict = {}  # 定义参数字典

    # 定义参数
    M = random.randint(2, 5)  # 蜂窝小区的数量
    N = np.random.randint(200, 800, M)  # 每个蜂窝小区中用户的数量
    K = np.random.randint(20, 40, M)  # 每个蜂窝小区中空闲设备的数量

    k_factory = 5 * 10 ** (-27)  # CPU芯片的能效系数

    # td_mi任务最大容忍延迟 ***
    t_mi_max = []
    for m in range(M):
        t_mi_max.append(np.random.uniform(0.05, 2, N[m]))

    # td_mi的任务所需CPU周期数
    c_mi_min = 0.5 * 10 ** 8  # td_mi的任务处理所需的最少CPU数量
    c_mi_max = 0.5 * 10 ** 9  # td_mi的任务处理所需的最多CPU数量
    c_mi = []
    for m in range(M):
        c_mi.append(np.random.uniform(c_mi_min, c_mi_max, N[m]))

    # td_mi的本地计算能力
    f_mi_min = 0.5 * 10 ** 8  # td_ij的本地计算资源最小值
    f_mi_max = 1 * 10 ** 9  # td_ij的本地计算资源最大值
    f_mi = []
    for m in range(M):
        f_mi.append(np.random.uniform(f_mi_min, f_mi_max, N[m]))

    f_m = 10 * 10 ** 10  # ES i的计算资源量 ***

    # td_mi任务的价值
    v_mi = []
    for m in range(M):
        v_mi.append(np.random.uniform(5, 10, N[m]))

    gamma = 1  # 单位能耗的成本
    W_B = 20 * 10 ** 6  # 20MHz，每个子信道的带宽
    N0 = 10 ** (-13)  # -100dBm 背景噪声功率

    # 每个td_mi受到的小区间干扰
    I_mi = []
    for m in range(M):
        I_mi.append(np.random.uniform(N0 * 10, N0 * 1000, N[m]))

    # 每个ad_mk受到的小区间干扰
    I_mk = []
    for m in range(M):
        I_mk.append(np.random.uniform(N0 * 10, N0 * 1000, K[m]))

    p_mi = 2  # 2W 每个td_mi的发射功率

    p_m = 20  # 20W BS的发射功率

    # 每个设备与BS之间的信道增益
    h_mi = []
    for m in range(M):
        h_mi.append(np.random.uniform(1 * 10 ** (-6), 1 * 10 ** (-4), N[m]))

    # td_mi的任务数据量
    L_mi_max = 5 * 10 ** 5  # 用户任务数据量最大值
    L_mi_min = 2 * 10 ** 5  # 用户任务数据量最小值
    L_mi = []
    for m in range(M):
        L_mi.append(np.random.uniform(L_mi_min, L_mi_max, N[m]))

    R_between_ES = np.random.uniform(1 * 10 ** 9, 1 * 10 ** 10, (M, M))  # 不同BS之间的数据传输速率

    # ad_mk的本地计算能力
    f_mk_min = 2 * 10 ** 9  # ad_mk的本地计算资源最小值
    f_mk_max = 6 * 10 ** 9  # ad_mk的本地计算资源最大值
    f_mk = []
    for m in range(M):
        f_mk.append(np.random.uniform(f_mk_min, f_mk_max, K[m]))

    # 每个ad_mk与BS之间的信道增益
    h_mk = []
    for m in range(M):
        h_mk.append(np.random.uniform(1 * 10 ** (-6), 1 * 10 ** (-4), K[m]))

    # 每个ad_mk对自己每个CPU周期的报价
    a_mk = []
    for m in range(M):
        a_mk.append(np.random.uniform(1 * 10 ** (-9), 1 * 10 ** (-8), K[m]))

    # td_mi将数据传输给BS的速率
    R_mi = []
    for m in range(M):
        R_mi.append(W_B * np.log2(1 + p_mi * h_mi[m] ** 2 / (N0 + I_mi[m])))

    # td_mi将数据传输给BS的时延
    t_mi_tran = []
    for m in range(M):
        t_mi_tran.append(L_mi[m] / R_mi[m])

    param_dict['M'] = M
    param_dict['N'] = N
    param_dict['K'] = K
    param_dict['k_factory'] = k_factory
    param_dict['t_mi_max'] = t_mi_max
    param_dict['c_mi'] = c_mi
    param_dict['f_mi'] = f_mi
    param_dict['f_m'] = f_m
    param_dict['v_mi'] = v_mi
    param_dict['gamma'] = gamma
    param_dict['W_B'] = W_B
    param_dict['N0'] = N0
    param_dict['I_mi'] = I_mi
    param_dict['I_mk'] = I_mk
    param_dict['p_mi'] = p_mi
    param_dict['p_m'] = p_m
    param_dict['h_mi'] = h_mi
    param_dict['L_mi'] = L_mi
    param_dict['R_between_ES'] = R_between_ES
    param_dict['f_mk'] = f_mk
    param_dict['h_mk'] = h_mk
    param_dict['a_mk'] = a_mk
    param_dict['R_mi'] = R_mi
    param_dict['t_mi_tran'] = t_mi_tran

    log_dict_to_file(param_dict, '../log/param.txt')
    return param_dict
