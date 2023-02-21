# from django.test import TestCase

# Create your tests here.
import multiprocessing


def processFun(queue,name):
    print(multiprocessing.current_process().pid,"进程放数据：",name)
    #将 name 放入队列
    queue.put(name)


if __name__ == '__main__':
    # 创建进程通信的Queue
    queue = multiprocessing.Queue()
    # 创建子进程
    process = multiprocessing.Process(target=processFun, args=(queue,[1,2,3,4]))
    process1 = multiprocessing.Process(target=processFun, args=(queue, {'a':1, 'b':4}))
    # 启动子进程
    process.start()
    process1.start()
    #该子进程必须先执行完毕
    process.join()
    process1.join()
    print(multiprocessing.current_process().pid,"取数据：")
    print(queue.get())
    print(queue.get())
