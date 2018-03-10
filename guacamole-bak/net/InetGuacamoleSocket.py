
import logging
import socket

from GuacamoleSocket import GuacamoleSocket
from guacamole.exceptions import GuacamoleUpstreamTimeoutException, GuacamoleServerException
from guacamole.io.ReaderGuacamoleReader import ReaderGuacamoleReader
from guacamole.io.WriterGuacamoleWriter import WriterGuacamoleWriter

class InetGuacamoleSocket(GuacamoleSocket):
    SOCKET_TIMEOUT = 15000

    def __init__(self, host, port):
        try:
            logging.debug('Connecting to guacd at %s:%d', host, port)
            self.socket = socket.create_connection((host, port), timeout=InetGuacamoleSocket.SOCKET_TIMEOUT)
            self.reader = ReaderGuacamoleReader(self.socket)
            self.writer = WriterGuacamoleWriter(self.socket)
        except socket.timeout as e:
            raise GuacamoleUpstreamTimeoutException(e)
        except socket.error as e:
            raise GuacamoleServerException(e)
        self._open = True

    def close(self):
        try:
            logging.debug('Closing connection to guacd.')
            self._open = False
            self.socket.close()
        except socket.error as e:
            raise GuacamoleServerException(e)

    def getReader(self):
        return self.reader

    def getWriter(self):
        return self.writer

    def isOpen(self):
        return self._open
