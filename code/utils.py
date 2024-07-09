# 日志打印

import logging


def log_dict_to_file(dictionary, file_path):
    # 创建新的日志记录器
    logger = logging.getLogger(__name__)

    # 移除之前的所有处理程序
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 配置日志
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(file_path, mode='w')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 遍历字典，将键值对写入日志
    for key, value in dictionary.items():
        logger.info(f"{key}: {value}")


def compare_vectors(vec1, vec2):
    # 比较两个向量，生成新的向量,如果vec1>vec2，则返回1，否则返回0
    compared_result = (vec1 > vec2).astype(int)
    return compared_result
