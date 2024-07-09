# 主要包括ESP效用、算法运行时间、任务完成率
from performanceIndicators import performanceIndicators
from utils import log_dict_to_file
import time

iterations = 100
esp_utility_sum = 0
task_complete_rate_sum = 0
algorithm_performance = {}

# 记录开始时间
start_time = time.time()

for i in range(iterations):
    utility = performanceIndicators()
    esp_utility_sum += utility['esp_utility']
    task_complete_rate_sum += utility['task_complete_rate']

# 记录结束时间
end_time = time.time()

# 计算代码的运行时间
execution_time = (end_time - start_time)/iterations
esp_utility_avg = esp_utility_sum / iterations
task_complete_rate_avg = task_complete_rate_sum / iterations
algorithm_performance['esp_utility'] = esp_utility_avg
algorithm_performance['execution_time'] = execution_time
algorithm_performance['task_complete_rate'] = task_complete_rate_avg
log_dict_to_file(algorithm_performance, '../log/algorithm_performance.txt')
