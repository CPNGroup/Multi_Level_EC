from utils import compare_vectors
import numpy as np
from utils import log_dict_to_file


def firstLevelDecision(param_dict):
    M = param_dict['M']
    c_mi = param_dict['c_mi']
    t_mi_max = param_dict['t_mi_max']
    f_mi = param_dict['f_mi']
    v_mi = param_dict['v_mi']
    gamma = param_dict['gamma']
    k_factory = param_dict['k_factory']
    W_B = param_dict['W_B']
    h_mi = param_dict['h_mi']
    I_mi = param_dict['I_mi']
    p_mi = param_dict['p_mi']
    N0 = param_dict['N0']
    L_mi = param_dict['L_mi']
    N = param_dict['N']
    t_mi_tran = param_dict['t_mi_tran']

    first_level_decision = {}

    # td_mi在本地处理任务时需要提供的最小计算资源
    f_mi_loc = []
    for m in range(M):
        f_mi_loc.append(c_mi[m] / t_mi_max[m])

    # 获取指示向量，代表该任务是否能在本地处理
    indicator_vector = []
    for m in range(M):
        indicator_vector.append(compare_vectors(f_mi[m], f_mi_loc[m]))

    # 用户本地处理任务时的效用
    u_mi_loc = []
    for m in range(M):
        u_mi_loc.append(indicator_vector[m] * (v_mi[m] - gamma * k_factory * f_mi_loc[m] ** 2 * c_mi[m]))

    # ES m处理该任务时需要提供的计算资源量 ***
    f_m_mi = []
    for m in range(M):
        f_m_mi.append(c_mi[m] / (t_mi_max[m] - t_mi_tran[m]))

    # 根据公式推导判断卸载决策：

    vector_tmp_1 = []
    for m in range(M):
        vector_tmp_1.append(v_mi[m] - gamma * p_mi * t_mi_tran[m] - u_mi_loc[m])

    vector_tmp_2 = []
    for m in range(M):
        vector_tmp_2.append(k_factory * f_m_mi[m] ** 2 * c_mi[m])

    # 第一级td_mi的临时卸载决策

    x_mi_opt_1 = []
    for m in range(M):
        x_mi_opt_1.append(compare_vectors(vector_tmp_1[m], vector_tmp_2[m]))

    # 计算对应的最佳费用
    alpha_mi_opt_1 = []
    for m in range(M):
        alpha_mi_opt_1.append(np.zeros(N[m]))

    for m in range(M):
        for i in range(N[m]):
            if x_mi_opt_1[m][i] == 1:
                tmp_1 = k_factory * f_m_mi[m][i] ** 2 * c_mi[m][i]
                tmp_2 = (v_mi[m][i] - gamma * p_mi * t_mi_tran[m][i] - u_mi_loc[m][i] + tmp_1) / 2
                tmp_3 = v_mi[m][i] - gamma * p_mi * t_mi_tran[m][i] - u_mi_loc[m][i]
                if tmp_1 < tmp_2 < tmp_3:
                    alpha_mi_opt_1[m][i] = tmp_2
                elif tmp_2 <= tmp_1:
                    alpha_mi_opt_1[m][i] = tmp_1
                else:
                    alpha_mi_opt_1[m][i] = tmp_3
            else:
                alpha_mi_opt_1[m][i] = 0

    # 第一级结束后暂时决定要卸载的任务索引
    task_index_1 = []
    for m in range(M):
        task_index_1.append([])

    # 所有要卸载的任务
    task_offload_num = 0
    for m in range(M):
        for i in range(N[m]):
            if x_mi_opt_1[m][i] == 1:
                task_index_1[m].append(i)
                task_offload_num += 1

    first_level_decision["task_index_1"] = task_index_1
    first_level_decision["alpha_mi_opt_1"] = alpha_mi_opt_1
    first_level_decision["x_mi_opt_1"] = x_mi_opt_1
    first_level_decision["f_m_mi"] = f_m_mi
    first_level_decision["u_mi_loc"] = u_mi_loc
    first_level_decision["task_offload_num"] = task_offload_num

    log_dict_to_file(first_level_decision, '../log/first_level_decision.txt')
    return first_level_decision
