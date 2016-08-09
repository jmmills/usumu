from . import Bus
from redis import StrictRedis


@Bus.register
class Redis(object):
    def publish(self, msg):
        pass
