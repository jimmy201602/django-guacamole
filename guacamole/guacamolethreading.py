# -*- coding: utf-8 -*-
import threading

def get_redis_instance():
    from django_guacamole.asgi import channel_layer
    return channel_layer._connection_list[0]

class GuacamoleThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    
    def __init__(self,message):
        super(GuacamoleThread, self).__init__()
        self._stop_event = threading.Event()
        self.message = message
        self.queue = self.redis_queue()
        
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def redis_queue(self):
        redis_instance = get_redis_instance()
        redis_sub = redis_instance.pubsub()
        redis_sub.subscribe(self.message.reply_channel.name)
        return redis_sub
            
    def run(self):
        #fix the first login 1 bug
        first_flag = True
        while (not self._stop_event.is_set()):
            text = self.queue.get_message()
            if text:
                if isinstance(data,(list,tuple)):
                    if data[0] == 'close':
                        self.stop()