class Function(object):
    def __init__(self, func, lower_bound, upper_bound, dimension = None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.dimension = dimension
        self.body = func

    def __call__(self, *args):
        return self.body(*args)