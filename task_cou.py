from task_result import task_test

s = task_test.delay(3, 6)
print(s.result)
