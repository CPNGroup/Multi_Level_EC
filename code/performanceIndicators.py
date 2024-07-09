from thirdLevelDecision import thirdLevelDecision
from paramGen import paramGen
from firstLevelDecision import firstLevelDecision
from secondLevelDecision import secondLevelDecision
from secondLevelTriggerJudgment import secondLevelTriggerJudgment
from overloadDeterminationAndTaskScreening import overloadDeterminationAndTaskScreening
from utils import log_dict_to_file
import numpy as np


def performanceIndicators():
    param_dict = paramGen()
    first_level_decision = firstLevelDecision(param_dict)
    overload_determination_task_screening_dict = overloadDeterminationAndTaskScreening(param_dict, first_level_decision)
    second_level_trigger_condition_judgment = secondLevelTriggerJudgment(param_dict,
                                                                         overload_determination_task_screening_dict)
    second_level_decision = secondLevelDecision(second_level_trigger_condition_judgment,
                                                overload_determination_task_screening_dict, param_dict,
                                                first_level_decision)
    third_level_decision = thirdLevelDecision(param_dict, first_level_decision, second_level_decision)
    task_process_location = third_level_decision['task_process_location']
    ad_utility_3 = third_level_decision['ad_utility_3']
    M = param_dict['M']
    N = param_dict['N']
    K = param_dict['K']
    u_mi_loc = first_level_decision['u_mi_loc']
    alpha_mi_opt_1 = first_level_decision["alpha_mi_opt_1"]
    gamma = param_dict['gamma']
    p_mi = param_dict['p_mi']
    t_mi_tran = param_dict['t_mi_tran']
    v_mi = param_dict['v_mi']
    f_m_mi = first_level_decision['f_m_mi']
    k_factory = param_dict['k_factory']
    c_mi = param_dict['c_mi']
    L_mi = param_dict['L_mi']
    R_between_ES = param_dict['R_between_ES']
    t_mi_max = param_dict['t_mi_max']
    task_ES_utility_3 = third_level_decision['task_ES_utility_3']
    task_index_3 = third_level_decision['task_index_3']

    utility = {}
    task_td_utility = []
    for m in range(M):
        task_td_utility.append(np.zeros(N[m]))

    task_ES_utility = []
    for m in range(M):
        task_ES_utility.append(np.zeros(N[m]))

    ad_utility = ad_utility_3

    for m in range(M):
        for i in range(N[m]):
            if task_process_location[m][i] == "local":
                task_td_utility[m][i] = u_mi_loc[m][i]
            elif task_process_location[m][i] == "ES" + str(m):
                task_td_utility[m][i] = v_mi[m][i] - alpha_mi_opt_1[m][i] - gamma * p_mi * t_mi_tran[m][i]
                task_ES_utility[m][i] = alpha_mi_opt_1[m][i] - k_factory * f_m_mi[m][i] ** 2 * c_mi[m][i]
            elif task_process_location[m][i].startswith("ES"):
                task_td_utility[m][i] = v_mi[m][i] - alpha_mi_opt_1[m][i] - gamma * p_mi * t_mi_tran[m][i]
                n = int(task_process_location[m][i][-1])
                t_m_to_n_tran = L_mi[m][i] / R_between_ES[m][n]
                f_m_to_n_need = c_mi[m][i] / (t_mi_max[m][i] - t_m_to_n_tran - t_mi_tran[m][i])
                task_ES_utility[m][i] = alpha_mi_opt_1[m][i] - k_factory * f_m_to_n_need ** 2 * c_mi[m][i]
            elif task_process_location[m][i].startswith("AD"):
                task_td_utility[m][i] = v_mi[m][i] - alpha_mi_opt_1[m][i] - gamma * p_mi * t_mi_tran[m][i]
                task_ES_utility[m][i] = task_ES_utility_3[m][i]

    # 获取每个小区中TD和AD效用的均值
    td_cell_avg_utility = np.zeros(M)
    ad_cell_avg_utility = np.zeros(M)
    for m in range(M):
        td_cell_avg_utility[m] = np.mean(task_td_utility[m])
        ad_cell_avg_utility[m] = np.mean(ad_utility[m])

    # 获取所有TD和AD效用的均值
    td_avg_utility = sum(td_cell_avg_utility) / M
    ad_avg_utility = sum(ad_cell_avg_utility) / M
    # 获取ESP的效用
    esp_utility = sum([np.sum(arr) for arr in task_ES_utility])

    # 任务完成率
    task_num_total = first_level_decision['task_offload_num']
    task_uncomplete_sum = 0
    for m in range(M):
        task_num_total += N[m]
        task_uncomplete_sum += len(task_index_3[m])

    task_complete_rate = (task_num_total - task_uncomplete_sum) / task_num_total

    utility["task_td_utility"] = task_td_utility
    utility["task_ES_utility"] = task_ES_utility
    utility["ad_utility"] = ad_utility
    utility["td_cell_avg_utility"] = td_cell_avg_utility
    utility["ad_cell_avg_utility"] = ad_cell_avg_utility
    utility["td_avg_utility"] = td_avg_utility
    utility["ad_avg_utility"] = ad_avg_utility
    utility["esp_utility"] = esp_utility
    utility["task_complete_rate"] = task_complete_rate
    log_dict_to_file(utility, "../log/utility.txt")
    return utility
