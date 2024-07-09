import numpy as np
from utils import log_dict_to_file


def overloadDeterminationAndTaskScreening(param_dict, first_level_decision):
    # 超载判断
    # 先计算每个小区的边缘服务器需要提供的计算资源量
    M = param_dict['M']
    f_m_mi = first_level_decision['f_m_mi']
    x_mi_opt_1 = first_level_decision['x_mi_opt_1']
    f_m = param_dict['f_m']
    task_index_1 = first_level_decision['task_index_1']
    alpha_mi_opt_1 = first_level_decision['alpha_mi_opt_1']
    k_factory = param_dict['k_factory']
    c_mi = param_dict['c_mi']
    N = param_dict['N']

    overload_determination_task_screening_dict = {}

    f_m_allocation = []
    for m in range(M):
        f_m_allocation.append(sum(x_mi_opt_1[m] * f_m_mi[m]))

    # 超载的指示向量
    indicator_vector_overload = np.zeros(M)
    # 超载的计算资源量
    f_m_overload = np.zeros(M)
    for m in range(M):
        if f_m_allocation[m] > f_m:
            indicator_vector_overload[m] = 1
            f_m_overload[m] = f_m_allocation[m] - f_m

    # 筛选出在其他位置处理的任务
    task_index_screened = []
    for m in range(M):
        task_index_screened.append([])

    # 初始化每个ES剩余可用的计算资源量
    f_m_1_left = np.zeros((M,))

    for m in range(M):
        if indicator_vector_overload[m] == 1:
            # 每个任务在ES上处理时给ES带来的效用(单位计算资源的效用)
            u_m_mi_1 = []
            for task_index in task_index_1[m]:
                u_m_mi_1.append(
                    (alpha_mi_opt_1[m][task_index] - k_factory * f_m_mi[m][task_index] ** 2 * c_mi[m][task_index]) /
                    f_m_mi[m][task_index])
            # 对列表进行降序排序，并获取排序后的索引
            sorted_indices = sorted(range(len(u_m_mi_1)), key=lambda x: u_m_mi_1[x], reverse=True)
            # 输出按降序排序的任务索引
            sorted_task_index_list = [task_index_1[m][i] for i in sorted_indices]
            # 开始筛选
            f_m_left = f_m
            for task_index in sorted_task_index_list:
                if f_m_mi[m][task_index] > f_m_left:
                    task_index_screened[m].append(task_index)
                else:
                    f_m_left = f_m_left - f_m_mi[m][task_index]
            f_m_1_left[m] = f_m_left
        else:
            f_m_1_left[m] = f_m - f_m_allocation[m]

    # 然后为已经确定的任务处理位置赋值（即在本地计算和确定了在主边缘服务器处理的任务）
    task_process_location = []
    for m in range(M):
        task_process_location.append(['unkown'] * N[m])
    for m in range(M):
        for i in range(N[m]):
            if x_mi_opt_1[m][i] == 0:
                task_process_location[m][i] = 'local'
            else:
                if not (i in task_index_screened[m]):
                    task_process_location[m][i] = 'ES' + str(m)

    overload_determination_task_screening_dict['task_process_location'] = task_process_location
    overload_determination_task_screening_dict['f_m_1_left'] = f_m_1_left
    overload_determination_task_screening_dict['task_index_screened'] = task_index_screened
    overload_determination_task_screening_dict['indicator_vector_overload'] = indicator_vector_overload
    overload_determination_task_screening_dict['f_m_overload'] = f_m_overload

    log_dict_to_file(overload_determination_task_screening_dict, '../log/overload_determination_task_screening.txt')
    return overload_determination_task_screening_dict
