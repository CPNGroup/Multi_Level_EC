from utils import log_dict_to_file


def secondLevelTriggerJudgment(param_dict, overload_determination_task_screening_dict):
    second_level_trigger_condition_judgment = {}

    M = param_dict['M']
    indicator_vector_overload = overload_determination_task_screening_dict['indicator_vector_overload']

    # 对蜂窝小区进行分类
    # 确定接收方和卸载方
    offload_cell = []
    receive_cell = []

    for m in range(M):
        if indicator_vector_overload[m] == 1:
            offload_cell.append(m)
        else:
            receive_cell.append(m)

    second_level_trigger = 1
    if len(offload_cell) == 0 or len(receive_cell) == 0:
        second_level_trigger = 0

    second_level_trigger_condition_judgment['second_level_trigger'] = second_level_trigger
    second_level_trigger_condition_judgment['offload_cell'] = offload_cell
    second_level_trigger_condition_judgment['receive_cell'] = receive_cell

    log_dict_to_file(second_level_trigger_condition_judgment, '../log/second_level_trigger_condition_judgment.txt')
    return second_level_trigger_condition_judgment
