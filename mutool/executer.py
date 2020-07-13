
def executeFunction(funcation,params:list,threadNumber:int = 10):
    import threadpool

    validateParams = []
    for item in params:
        if isinstance(item,list):
            item = (item,None)
            validateParams.append(item)
        else:
            validateParams.append(item)

    taskPool = threadpool.ThreadPool(threadNumber)
    spiders = threadpool.makeRequests(funcation, validateParams)
    for spider in spiders:
        taskPool.putRequest(spider)
    taskPool.wait()