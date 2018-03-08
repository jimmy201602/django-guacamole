from gevent import monkey
monkey.patch_all()

import threading
from geventwebsocket import WebSocketApplication
from geventwebsocket.protocols.base import BaseProtocol
import logging
from guacamole.net.SimpleGuacamoleTunnel import SimpleGuacamoleTunnel
from guacamole.net.InetGuacamoleSocket import InetGuacamoleSocket
from guacamole.net.GuacamoleTunnel import GuacamoleTunnel
from guacamole.protocol.ConfiguredGuacamoleSocket import ConfiguredGuacamoleSocket
from guacamole.protocol.GuacamoleConfiguration import GuacamoleConfiguration
from guacamole.protocol.GuacamoleInstruction import GuacamoleInstruction
from guacamole.protocol.GuacamoleStatus import GuacamoleStatus

class GuacamoleProtocol(BaseProtocol):
    PROTOCOL_NAME = 'guacamole'

class GuacamoleWebsocketRelay(WebSocketApplication):
    BUFFER_SIZE = 8192
    protocol_class = GuacamoleProtocol

    def __init__(self, ws):
        super(GuacamoleWebsocketRelay, self).__init__(ws)
        logging.info("Created new GuacamoleWebSocketRelay, %s", self)

    def on_open(self):
        logging.info("Connection!")
        current_client = self.ws.handler.active_client
        try:
            guacamole_server = InetGuacamoleSocket("172.17.0.2", 4822)
            session_configuration = GuacamoleConfiguration("vnc")
            session_configuration.setParameter("hostname", "192.168.152.131")
            session_configuration.setParameter("port", "5901")
            session_configuration.setParameter("username", "root")
            session_configuration.setParameter("password", "l251008549")

            current_client.tunnel = SimpleGuacamoleTunnel(
                socket=ConfiguredGuacamoleSocket(guacamole_server, session_configuration)
            )
        except Exception as e:
            logging.exception("Creation of tunnel to guacd daemon failed")
            closeConnection(self.ws, e)

        readThread = _ReaderThread(self.ws, current_client.tunnel)
        readThread.start()
        logging.info("Reader thread started")

    def on_message(self, message):
        if message is None:
            return

        current_client = self.ws.handler.active_client
        if not current_client.tunnel:
            return

        tunnel = current_client.tunnel
        writer = tunnel.acquireWriter()
        try:
            writer.write(message)
        except Exception as e:
            logging.exception('Unable to write to tunnel, closing connection')
            closeConnection(self.ws, e)
        tunnel.releaseWriter()

    def on_close(self, reason):
        logging.info("Connection closed :'(")
        current_client = self.ws.handler.active_client
        if current_client.tunnel and current_client.tunnel.isOpen():
            try:
                current_client.tunnel.close()
            except Exception as e:
                logging.error("Unable to close guacamole tunnel: %s", current_client.tunnel)


def closeConnection(websocket, status):
    wsStatusCode = status.websocket_status
    guacStatusCode = str(status.guacamole_status)
    try:
        websocket.close(wsStatusCode, guacStatusCode)
    except:
        pass


class _ReaderThread(threading.Thread):
    def __init__(self, websocket, tunnel):
        super(_ReaderThread, self).__init__()
        self.tunnel = tunnel
        self.websocket = websocket
        self.buffer = bytearray(0)

    def run(self):
        reader = self.tunnel.acquireReader()
        self.websocket.send(str(GuacamoleInstruction(GuacamoleTunnel.INTERNAL_DATA_OPCODE, self.tunnel.getUUID())))
        readMessage = reader.read()
        while readMessage:
            self.buffer.extend(readMessage)
            if not reader.available() or len(self.buffer) >= GuacamoleWebsocketRelay.BUFFER_SIZE:
                self.websocket.send(self.buffer, False)
                del self.buffer[:]
            readMessage = reader.read()
        closeConnection(self.websocket, '200')
