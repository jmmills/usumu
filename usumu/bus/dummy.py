from . import Bus


@Bus.register
class DummyBus(object):
    def publish(self, msg):
        pass