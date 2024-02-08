def copy_result(func):
    def deco(*args, **kwargs):
        return func(*args, **kwargs).copy()
    return deco


def singleton(_class_):
    def deco(*args, **kwargs):
        class_ = _class_.__class__.mro(_class_)[0]
        def create():
            class_.__instance__ = _class_(*args, **kwargs)
            return class_.__instance__
        return class_.__instance__ if hasattr(class_, "__instance__") else create()
    return deco