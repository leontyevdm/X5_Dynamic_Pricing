import os


DEBUG = False
LOCAL = False

def getDEBUG():
    global DEBUG
    return DEBUG

def setDEBUG(bool):
    global DEBUG
    DEBUG = bool

def getLOCAL():
    global LOCAL
    return LOCAL

def setLOCAL(bool):
    global LOCAL
    LOCAL = bool

def is_under_debugging():
    return 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ and os.environ['PYDEVD_LOAD_VALUES_ASYNC'] == 'True' \
            and 'PYTHONDONTWRITEBYTECODE' in os.environ and os.environ['PYTHONDONTWRITEBYTECODE'] == '1'

# def debug_print_func_name(func):
#     @functools.wraps(func)
#     def wrapped(*args, **kwargs):
#         print(func.__name__)
#
#         return func(*args, **kwargs)
#
#     return wrapped