from . import Bus


@Bus.register
class Dummy(object):
    def publish(self, msg):
        pass