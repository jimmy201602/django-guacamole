
import uuid

from AbstractGuacamoleTunnel import AbstractGuacamoleTunnel


class SimpleGuacamoleTunnel(AbstractGuacamoleTunnel):
    def __init__(self, socket):
        self.uuid = str(uuid.uuid4())
        self.socket = socket
        super(SimpleGuacamoleTunnel, self).__init__()

    def getSocket(self):
        return self.socket

    def getUUID(self):
        return self.uuid

