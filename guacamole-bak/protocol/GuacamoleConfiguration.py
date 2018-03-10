

class GuacamoleConfiguration(object):
    def __init__(self, protocol=None):
        self.connectionID = None
        self.protocol = protocol
        self.parameters = {}

    @property
    def connectionID(self):
        return self._connectionID

    @connectionID.setter
    def connectionID(self, connectionID):
        self._connectionID = connectionID

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        self._protocol = protocol

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    def getParameter(self, paramName):
        return self._parameters.get(paramName, None)

    def delParameter(self, paramName):
        del self._parameters[paramName]

    def setParameter(self, paramName, paramValue):
        self._parameters[paramName] = paramValue

