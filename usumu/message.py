from time import time
from .logger import DummyLogger
from .bus.dummy import DummyBus
from .seralizer import DummySerializer


class Message:
    def __init__(self, transaction, bus=DummyBus(),
                 serializer=DummySerializer(), ns=None, merge=False):
        self.__transaction = transaction
        self.__serializer = serializer
        self.__bus = bus
        self.__merge = merge
        self.__ns = ns

    @property
    def transaction(self):
        return self.__transaction

    @property
    def serializer(self):
        return self.__serializer

    @property
    def bus(self):
        return self.__bus

    @property
    def merge(self):
        return self.__merge

    @property
    def name(self):
        if self.__ns:
            return self.__ns + '.' + self.transaction.short_name
        else:
            return self.transaction.name

    def base_dict(self):
        return {
            'name': self.message_name,
            'ts': time,
            'completed': self.transaction.completed,
            'error': False,
            'input': {
                'args': self.transaction.args,
                'kwargs': self.transaction.kwargs
            }
        }

    def exception_dict(self, msg={}):
        if self.transaction.completed and self.transaction.raised:
            msg['error'] = True
            msg['exception'] = None  # Todo setup exception structure

    def completed_dict(self, msg={}):
        if self.transaction.completed and not self.transaction.raised:
            msg['output'] = self.transaction.returned

    def __dict__(self):
        payload = self.base_dict()
        self.exception_dict(payload)
        self.completed_dict(payload)
        return payload

    def send(self):
        if self.merge and not self.transaction.completed:
            return None

        msg = self.serializer.encode(self)
        self.bus.publish(msg)

        return msg
