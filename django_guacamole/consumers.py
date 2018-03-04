# -*- coding: utf-8 -*-
from channels.generic.websockets import WebsocketConsumer
try:
    import simplejson as json
except ImportError:
    import json
import sys
from django.utils.encoding import smart_unicode
from guacamole.guacamolethreading import get_redis_instance

class GuacamoleWebsocket(WebsocketConsumer):
    
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True   

    
    def connect(self, message):
        self.message.reply_channel.send({"accept": True})
        self.message.reply_channel.send({"text":json.dumps(['channel_name',self.message.reply_channel.name])},immediately=True)
        
    def disconnect(self, message):
        #close threading       
        self.message.reply_channel.send({"accept":False})
        self.closeguacamole()
    
    def queue(self):
        queue = get_redis_instance()
        channel = queue.pubsub()
        return queue
    
    def closeguacamole(self):
        #close threading
        self.queue().publish(self.message.reply_channel.name, json.dumps(['close']))
        
    def receive(self,text=None, bytes=None, **kwargs):
        print 11,text
        self.queue().publish(self.message.reply_channel.name, json.loads(text)[1])