from functools import wraps
from envcfg.smart import usumu as config

from .transaction import TransactionFactory
from .message import Message


class Usumu:
    def __init__(self, name, merge=True, log=False, bus='Dummy', msg='Dummy', logger='Dummy'):
        self._logger = None

        self.name = name
        self.merge = merge
        self.log = log
        self.bus = bus
        self.msg = msg
        self.logger = logger
        self.__tf = TransactionFactory(scope=self, on_call=self.on_call,
                                       on_raise=self.on_raise, on_return=self.on_return)

    @property
    def transactions(self):
        return self.__tf

    @property.getter
    def logger(self):
        return self._logger

    @property.setter
    def logger(self, value):
        _set_or_load_and_instantiate(self, '_logger', value)

    @property.getter
    def bus(self):
        return self._bus

    @property.setter
    def bus(self, value):
        _set_or_load_and_instantiate(self, '_bus', value)

    @property.getter
    def msg(self):
        return self._msg

    @property.setter
    def msg(self, value):
        _set_or_load_and_instantiate(self, '_msg', value)

    def on_call(self, transaction):
        msg = Message(transaction)



    def on_raise(self, transaction):
        pass

    def on_return(self, transaction):
        pass

    def emit(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            this_transaction = self.transactions.new(func=func, args=args, kwargs=kwargs)
            return this_transaction()
        return decorated


def _set_or_load_and_instantiate(obj, attr, value):
    v = None
    if not getattr(obj, attr):
        if isinstance(value):
            v = value
        else:
            __import__(value)
            v = value()
        setattr(obj, attr, v)


