from abc import ABCMeta


class Logger(metaclass=ABCMeta):
    pass


class Default(Logger):  # default logger driver is a dummy driver and does nothing
    pass
