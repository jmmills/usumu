from time import time
from abc import ABCMeta, abstractmethod


class MessageFactory:  # Add instance validation for our delegates
    def __init__(self, bus=object(), serializer=object(), msg_class=Message, ns=None, merge=False):
        self._bus = bus
        self._serializer = serializer
        self._ns = ns
        self._merge = merge
        self._msg_class = msg_class

    def new(self, transaction):
        return self._msg_class(bus=self._bus, seralizer=self._serializer,
                               ns=self._ns, merge=self._merge, transaction=transaction)


class Message(metaclass=ABCMeta):  # Add instance validation for our delegates
    def __init__(self, transaction, bus=object(),
                 serializer=object(), ns=None, merge=False):
        self.__transaction = transaction
        self.__serializer = serializer
        self.__bus = bus
        self.__merge = merge
        self.__ns = ns
        self.__payload = {}

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

    @property.get
    def payload(self):
        return self.__payload

    @property.set
    def payload(self, payload):
        assert isinstance(payload, dict)
        self.__payload = payload

    def __dict__(self):  # handle merge or not merged logic
        self.initialize_payload()

        if self.transaction.completed and self.transaction.raised:
            self.augment_payload_for_exception()

        if self.transaction.completed and not self.transaction.raised:
            self.augment_payload_when_finished()

        return self.payload

    def send(self):
        if self.merge and not self.transaction.completed:
            return None

        msg = self.serializer.encode(self)
        self.bus.publish(msg)

        return msg

    @abstractmethod
    def initialize_payload(self):
        pass

    @abstractmethod
    def augment_payload_for_exception(self, payload={}):
        pass

    @abstractmethod
    def augment_payload_when_finished(self, payload={}):
        pass


# we need to implement an abstract base class here?
class Default(Message):

    @staticmethod
    def initialize_payload(self):
        return {
            'name': self.transaction.name,
            'ns': self.transaction.ns,
            'ts': time,
            'completed': self.transaction.completed,
            'error': False,
            'input': {
                'args': self.transaction.args,
                'kwargs': self.transaction.kwargs
            }
        }

    @staticmethod
    def augment_payload_for_exception(self):  # Todo finish writing this
        self.payload['error'] = True
        self.payload['exception'] = None  # Todo setup exception structure

    @staticmethod
    def augment_payload_when_finished(self, payload={}):  # Finish writing this
        self.payload['output'] = self.transaction.returned

