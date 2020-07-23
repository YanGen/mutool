import time,sys
# 几个方法增强
# 打印日志
def log(text="execute => "):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

# 睡眠
def sleep(second=1):
    def decorator(func):
        def wrapper(*args, **kw):
            time.sleep(second)
            return func(*args, **kw)
        return wrapper
    return decorator

# 错误重尝
def retry(count=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    ans = func(*args, **kwargs)
                    return ans
                except Exception as e:
                    ex = e
            raise ex
        return wrapper
    return decorator


def tryfun(printdebug=True):
    def inner1(f):
        def inner2(*args, **kwargs):
            try:
                res = f(*args, **kwargs)
            except Exception as err:
                if printdebug:
                    info = sys.exc_info()[2].tb_frame.f_back
                    temp = "filename:{}\nlines:{}\tfuncation:{}\terror:{}"
                    print(temp.format(info.f_code.co_filename, info.f_lineno, f.__name__, repr(err)))
                res = None
            return res
        return inner2
    return inner1