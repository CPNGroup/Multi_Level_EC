import numpy as np
from utils import log_dict_to_file


def thirdLevelDecision(param_dict, first_level_decision, second_level_decision):
    M = param_dict['M']
    N0 = param_dict['N0']
    W_B = param_dict['W_B']
    p_m = param_dict['p_m']
    h_mk = param_dict['h_mk']
    I_mk = param_dict['I_mk']
    f_mk = param_dict['f_mk']
    task_index_3 = second_level_decision['task_index_3']
    N = param_dict['N']
    K = param_dict['K']
    L_mi = param_dict['L_mi']
    t_mi_max = param_dict['t_mi_max']
    c_mi = param_dict['c_mi']
    t_mi_tran = param_dict['t_mi_tran']
    gamma = param_dict['gamma']
    alpha_mi_opt_1 = first_level_decision['alpha_mi_opt_1']
    a_mk = param_dict['a_mk']
    task_process_location = second_level_decision['task_process_location']

    third_level_decision = {}

    # BS将数据传输给ad_mk的速率
    R_mk = []
    for m in range(M):
        R_mk.append(W_B * np.log2(1 + p_m * h_mk[m] ** 2 / (N0 + I_mk[m])))

    # 初始化各个ADs剩余的计算资源量
    f_mk_left = f_mk
    # 初始化第三级决策中每个任务给ES带来的效用
    task_ES_utility_3 = []
    for m in range(M):
        task_ES_utility_3.append(np.zeros(N[m]))
    # 初始化每个ADs的收益
    ad_utility_3 = []
    for m in range(M):
        ad_utility_3.append(np.zeros(K[m]))
    for m in range(M):
        if len(task_index_3[m]) == 0:
            continue
        else:
            # 对ADs的索引以及报价按照报价的升序排列
            sorted_indices = sorted(range(len(a_mk[m])), key=lambda x: a_mk[m][x])
            sorted_ad_mk = [a_mk[m][i] for i in sorted_indices]
            print("第", m, "个小区开始第三级调度决策")
            # 先计算任务对每个ADs的报价
            for task_index in task_index_3[m]:

                # 计算该任务到每个AD的传输时间
                t_mk_tran = L_mi[m][task_index] / R_mk[m]
                # 计算在各个AD剩余的计算时间
                t_left_comp = t_mi_max[m][task_index] - t_mi_tran[m][task_index] - t_mk_tran
                # 计算各个AD需要为该任务提供的计算资源量
                f_mk_need = c_mi[m][task_index] / t_left_comp
                # 计算传输开销
                cost_mk_tran = gamma * p_m * t_mk_tran
                # 计算ES留给各个ADs计算资源的报价
                alpha_mi_left = alpha_mi_opt_1[m][task_index] - cost_mk_tran
                # 计算ES对各个ADs单位CPU周期的报价
                b_mk_per_cpu = alpha_mi_left / c_mi[m][task_index]
                # print("第",m,"个小区第",task_index,"个任务对各个AD的报价:",b_mk_per_cpu)
                for k in range(len(sorted_ad_mk) - 1):
                    if f_mk_left[m][sorted_indices[k]] >= f_mk_need[sorted_indices[k]] and \
                            b_mk_per_cpu[sorted_indices[k]] > sorted_ad_mk[k + 1]:
                        task_process_location[m][task_index] = 'AD' + str(m) + "_" + str(sorted_indices[k])
                        f_mk_left[m][sorted_indices[k]] = f_mk_left[m][sorted_indices[k]] - f_mk_need[sorted_indices[k]]
                        task_index_3[m].remove(task_index)
                        task_ES_utility_3[m][task_index] = (b_mk_per_cpu[sorted_indices[k]] - sorted_ad_mk[k + 1]) * \
                                                           f_mk_need[
                                                               sorted_indices[k]]
                        ad_utility_3[m][sorted_indices[k]] = ad_utility_3[m][sorted_indices[k]] + (
                                sorted_ad_mk[k + 1] - sorted_ad_mk[k]) * f_mk_need[sorted_indices[k]]
                        break
                # 第三级调度决策后每个任务对ES的效用和ADs的效用
                # print("task_utility:",task_utility)
                # print("ad_utility:",ad_utility)

    third_level_decision['task_ES_utility_3'] = task_ES_utility_3
    third_level_decision['ad_utility_3'] = ad_utility_3
    third_level_decision['task_index_3'] = task_index_3
    third_level_decision['task_process_location'] = task_process_location

    log_dict_to_file(third_level_decision, '../log/third_level_decision.txt')
    return third_level_decision
