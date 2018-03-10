# -*- coding: utf-8 -*-
from channels.generic.websockets import WebsocketConsumer
import threading
import logging
from guacamole.net.SimpleGuacamoleTunnel import SimpleGuacamoleTunnel
from guacamole.net.InetGuacamoleSocket import InetGuacamoleSocket
from guacamole.net.GuacamoleTunnel import GuacamoleTunnel
from guacamole.protocol.ConfiguredGuacamoleSocket import ConfiguredGuacamoleSocket
from guacamole.protocol.GuacamoleConfiguration import GuacamoleConfiguration
from guacamole.protocol.GuacamoleInstruction import GuacamoleInstruction
from guacamole.protocol.GuacamoleStatus import GuacamoleStatus
try:
    import simplejson as json
except ImportError:
    import json
import ast
from django.conf import settings

def get_redis_instance():
    from django_guacamole.asgi import channel_layer
    return channel_layer._connection_list[0]

class GuacamoleWebsocket(WebsocketConsumer):
    
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True   

    
    def connect(self, message):
        self.message.reply_channel.send({"accept": True})
        logging.info("Connection!")
        try:
            guacamole_server = InetGuacamoleSocket(settings.GUACD_HOST, settings.GUACD_PORT)
            session_configuration = GuacamoleConfiguration("rdp")
            session_configuration.setParameter("hostname", settings.SSH_HOST)
            session_configuration.setParameter("port", settings.SSH_PORT)
            session_configuration.setParameter("username", settings.SSH_USER)
            session_configuration.setParameter("password", settings.SSH_PASSWORD)

            tunnel = SimpleGuacamoleTunnel(
                socket=ConfiguredGuacamoleSocket(guacamole_server, session_configuration)
            )
        except Exception as e:
            logging.exception("Creation of tunnel to guacd daemon failed")
            closeConnection(self.message, e)

        readThread = _ReaderThread(self.message, tunnel)
        readThread.start()
        logging.info("Reader thread started")
        
        writeThread = _WriterThread(self.message, tunnel)
        writeThread.start()
        logging.info("Writer thread started")
        
    def disconnect(self, message):
        #close threading
        logging.info('disconnect')
        self.message.reply_channel.send({"accept":False})
    
    def queue(self):
        queue = get_redis_instance()
        channel = queue.pubsub()
        return queue    

    def receive(self,text=None, bytes=None, **kwargs):
        self.queue().publish(self.message.reply_channel.name,text)
        #self.queue().publish(self.message.reply_channel.name, text)

def closeConnection(websocket, status):
    try:
        wsStatusCode = status.websocket_status
        guacStatusCode = str(status.guacamole_status)        
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
        from django_guacamole.asgi import channel_layer
        reader = self.tunnel.acquireReader()
        #self.websocket.send(str(GuacamoleInstruction(GuacamoleTunnel.INTERNAL_DATA_OPCODE, self.tunnel.getUUID())))
        channel_layer.send(self.websocket.reply_channel.name,{"text":str(GuacamoleInstruction(GuacamoleTunnel.INTERNAL_DATA_OPCODE, self.tunnel.getUUID()))})
        readMessage = reader.read()
        while readMessage:
            self.buffer.extend(readMessage)
            if not reader.available() or len(self.buffer) >= 8192:
                #self.websocket.send(self.buffer, False)
                #print self.buffer
                channel_layer.send(self.websocket.reply_channel.name,{"text":self.buffer})
                del self.buffer[:]
            readMessage = reader.read()
        closeConnection(self.websocket, '200')


class _WriterThread(threading.Thread):
    def __init__(self, websocket, tunnel):
        super(_WriterThread, self).__init__()
        self.tunnel = tunnel
        self.websocket = websocket
        self.buffer = bytearray(0)
        self.queue = self.redis_queue()
    
    def redis_queue(self):
        redis_instance = get_redis_instance()
        redis_sub = redis_instance.pubsub()
        redis_sub.subscribe(self.websocket.reply_channel.name)
        return redis_sub

    def run(self):
        while True:
            text = self.queue.get_message()
            if text is not None:
                try:
                    text = text['data']
                except Exception,e:
                    text = text
                #print 'sub message',text
                if isinstance(text,(long,int)) and text == 1:
                    pass
                else:
                    tunnel = self.tunnel
                    writer = tunnel.acquireWriter()
                    try:
                        writer.write(text)
                    except Exception as e:
                        logging.exception('Unable to write to tunnel, closing connection')
                        closeConnection(self.websocket, e)
                    tunnel.releaseWriter()