
DEV_MODE = False
LOCAL_MODE = False

def get_flag_DEV_MODE():
    global DEV_MODE
    return DEV_MODE

def set_flag_DEV_MODE(bool):
    global DEV_MODE
    DEV_MODE = bool

def get_flag_LOCAL_MODE():
    global LOCAL_MODE
    return LOCAL_MODE

def set_flag_LOCAL_MODE(bool):
    global LOCAL_MODE
    LOCAL_MODE = bool
