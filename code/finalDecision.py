from utils import log_dict_to_file


def finalDecision(param_dict, third_level_decision):
    final_decision = {}

    task_index_3 = third_level_decision["task_index_3"]
    task_process_location = third_level_decision["task_process_location"]
    M = param_dict["M"]
    # 最后将所有unknown的任务置为local
    for m in range(M):
        for task_index in task_index_3[m]:
            task_process_location[m][task_index] = 'local'

    final_decision["task_process_location"] = task_process_location
    log_dict_to_file(final_decision, "../log/final_decision.txt")
    return final_decision
