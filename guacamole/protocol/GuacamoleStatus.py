
# http code, websocket code, guacamole code
class GuacamoleStatus(object):
    def __init__(self, http_code, websocket_code, guacamole_code):
        self._http_code = http_code
        self._websocket_code = websocket_code
        self._guacamole_code = guacamole_code

    @property
    def http_code(self):
        return self._http_code

    @property
    def websocket_code(self):
        return self._websocket_code

    @property
    def guacamole_code(self):
        return self._guacamole_code

_guacamole_status_codes = {
    # The operation succeeded.
    'SUCCESS': [200, 1000, 0x0000],

    # The requested operation is unsupported.
    'UNSUPPORTED': [501, 1011, 0x0100],

    # The operation could not be performed due to an internal failure.
    'SERVER_ERROR': [500, 1011, 0x0200],

    # The operation could not be performed as the server is busy.
    'SERVER_BUSY': [503, 1008, 0x0201],

    # The operation could not be performed because the upstream server is not
    # responding.
    'UPSTREAM_TIMEOUT': [504, 1011, 0x0202],

    # The operation was unsuccessful due to an error or otherwise unexpected
    # condition of the upstream server.
    'UPSTREAM_ERROR': [502, 1011, 0x0203],

    # The operation could not be performed as the requested resource does not
    # exist.
    'RESOURCE_NOT_FOUND': [404, 1002, 0x0204],

    # The operation could not be performed as the requested resource is already
    # in use.
    'RESOURCE_CONFLICT': [409, 1008, 0x0205],

    # The operation could not be performed as the requested resource is now
    # closed.
    'RESOURCE_CLOSED': [404, 1002, 0x0206],

    # The operation could not be performed because the upstream server does
    # not appear to exist.
    'UPSTREAM_NOT_FOUND': [502, 1011, 0x0207],

    # The operation could not be performed because the upstream server is not
    # available to service the request.
    'UPSTREAM_UNAVAILABLE': [502, 1011, 0x0208],

    # The session within the upstream server has ended because it conflicted
    # with another session.
    'SESSION_CONFLICT': [409, 1008, 0x0209],

    # The session within the upstream server has ended because it appeared to
    # be inactive.
    'SESSION_TIMEOUT': [408, 1002, 0x020A],

    # The session within the upstream server has been forcibly terminated.
    'SESSION_CLOSED': [404, 1002, 0x020B],

    # The operation could not be performed because bad parameters were given.
    'CLIENT_BAD_REQUEST': [400, 1002, 0x0300],

    # Permission was denied to perform the operation, as the user is not yet
    # authorized ': [not yet logged in, for example]. As HTTP 401 has implications
    # for HTTP-specific authorization schemes, this status continues to map to
    # HTTP 403 ': ["Forbidden"]. To do otherwise would risk unintended effects.
    'CLIENT_UNAUTHORIZED': [403, 1008, 0x0301],

    # Permission was denied to perform the operation, and this operation will
    # not be granted even if the user is authorized.
    'CLIENT_FORBIDDEN': [403, 1008, 0x0303],

    # The client took too long to respond.
    'CLIENT_TIMEOUT': [408, 1002, 0x0308],

    # The client sent too much data.
    'CLIENT_OVERRUN': [413, 1009, 0x030D],

    # The client sent data of an unsupported or unexpected type.
    'CLIENT_BAD_TYPE': [415, 1003, 0x030F],

    # The operation failed because the current client is already using too
    # many resources.
    'CLIENT_TOO_MANY': [429, 1008, 0x031D]
}

for status, codes in _guacamole_status_codes.items():
    setattr(GuacamoleStatus, status, GuacamoleStatus(*codes))

