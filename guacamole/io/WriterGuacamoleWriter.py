
from guacamole.exceptions import GuacamoleUpstreamTimeoutException, GuacamoleServerException
from GuacamoleWriter import GuacamoleWriter

class WriterGuacamoleWriter(GuacamoleWriter):
    def __init__(self, socket):
        self.socket = socket

    def write(self, chunk):
        self.socket.sendall(chunk)

        # except socket.timeout as e:
        #     raise GuacamoleUpstreamTimeoutException(e)
        # except socket.error as e:
        #     raise GuacamoleServerException(e)

    def writeInstruction(self, instruction):
        self.write(str(instruction))

