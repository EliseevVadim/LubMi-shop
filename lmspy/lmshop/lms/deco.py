def copy_result(func):
    def deco(*args, **kwargs):
        return func(*args, **kwargs).copy()
    return deco

