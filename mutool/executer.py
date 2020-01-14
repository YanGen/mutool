import threading
import threadpool


def executeFunction(funcation,params,threadNumber:int = 10):
    taskPool = threadpool.ThreadPool(threadNumber)
    spiders = threadpool.makeRequests(funcation, params)
    for spider in spiders:
        taskPool.putRequest(spider)
    taskPool.wait()