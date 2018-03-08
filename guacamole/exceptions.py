from guacamole.protocol.GuacamoleStatus import GuacamoleStatus

class GuacamoleException(Exception):
    def getStatus(self):
        return GuacamoleStatus.SERVER_ERROR

class GuacamoleServerException(GuacamoleException):
    pass

class GuacamoleUpstreamException(GuacamoleException):
    def getStatus(self):
        return GuacamoleStatus.UPSTREAM_ERROR

class GuacamoleUpstreamTimeoutException(GuacamoleUpstreamException):
    def getStatus(self):
        return GuacamoleStatus.UPSTREAM_TIMEOUT

