import copy
from utils import log_dict_to_file


def secondLevelDecision(second_level_trigger_condition_judgment,  overload_determination_task_screening_dict, param_dict, first_level_decision):
    second_level_decision = {}
    second_level_trigger = second_level_trigger_condition_judgment["second_level_trigger"]
    offload_cell = second_level_trigger_condition_judgment["offload_cell"]
    receive_cell = second_level_trigger_condition_judgment["receive_cell"]
    task_index_screened = overload_determination_task_screening_dict["task_index_screened"]
    f_m_overload = overload_determination_task_screening_dict["f_m_overload"]
    f_m_1_left = overload_determination_task_screening_dict["f_m_1_left"]
    R_between_ES = param_dict["R_between_ES"]
    L_mi = param_dict["L_mi"]
    c_mi = param_dict["c_mi"]
    t_mi_max = param_dict["t_mi_max"]
    t_mi_tran = param_dict["t_mi_tran"]
    alpha_mi_opt_1 = first_level_decision["alpha_mi_opt_1"]
    gamma = param_dict["gamma"]
    k_factory = param_dict["k_factory"]
    task_process_location = overload_determination_task_screening_dict["task_process_location"]

    # 初始化参与第三级任务调度的索引
    task_index_3 = copy.deepcopy(task_index_screened)
    f_m_2_left = copy.deepcopy(f_m_1_left)
    if second_level_trigger == 1:
        print("第二级触发条件满足")
        # 先确定小区的优先级(卸载小区的优先级，超载的计算资源量越多的小区的优先级越高)
        f_m_overload_2 = []
        for m in offload_cell:
            f_m_overload_2.append(f_m_overload[m])
        # 对列表进行降序排序，并获取排序后的索引
        sorted_indices = sorted(range(len(f_m_overload_2)), key=lambda x: f_m_overload_2[x], reverse=True)
        # 输出按降序排序的任务索引
        # 卸载小区索引优先级排序
        sorted_offload_cell_index_list = [offload_cell[i] for i in sorted_indices]

        # 开始第二级任务调度
        for m in sorted_offload_cell_index_list:
            # 开始对要卸载目的地进行优先级排序
            # 拿到从当前小区到各个卸载目的地小区的速率
            R_m_to_receive_cell = R_between_ES[m][receive_cell]

            sorted_indices = sorted(range(len(R_m_to_receive_cell)), key=lambda x: R_m_to_receive_cell[x], reverse=True)
            sorted_receive_cell_index_list = [receive_cell[i] for i in sorted_indices]

            # 开始确定每个任务的处理位置，并且筛选出参与第三级调度的任务
            for i in task_index_screened[m]:
                for n in sorted_receive_cell_index_list:
                    # 计算卸载到该小区需要的计算资源量
                    t_m_to_n_tran = L_mi[m][i] / R_between_ES[m][n]
                    f_m_to_n_need = c_mi[m][i] / (t_mi_max[m][i] - t_m_to_n_tran - t_mi_tran[m][i])
                    # 还要计算效用是否非负，仿真时忽略了源BS的数据转发能耗
                    u_m_to_n = alpha_mi_opt_1[m][i] - gamma * k_factory * f_m_to_n_need ** 2 * c_mi[m][i]
                    if f_m_to_n_need <= f_m_2_left[n] and u_m_to_n > 0:
                        # print("第二级调度成功")
                        task_process_location[m][i] = 'ES' + str(n)
                        f_m_2_left[n] = f_m_2_left[n] - f_m_to_n_need
                        task_index_3[m].remove(i)
                        break

    second_level_decision["task_index_3"] = task_index_3
    second_level_decision["f_m_2_left"] = f_m_2_left
    second_level_decision["task_process_location"] = task_process_location
    log_dict_to_file(second_level_decision, "../log/second_level_decision.txt")
    return second_level_decision
