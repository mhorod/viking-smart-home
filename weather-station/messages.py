from abc import ABC, abstractmethod
import time

class Message:
    def __init__(self, text, message_type):
        self.text = text
        self.message_type = message_type

class HasTimeLimit(ABC):
    def __init__(self, text, time_to_live):
        self.text = text

    def get_time_to_live(self):
        return time_to_live

class MessageQueue:
    def __init__(self):
        self.type_limits = {}
        self.messages_by_type = {}
        self.next_message_id = 0

    def set_type_limit(self, message_type, amount_limit):
        self.type_limits[message_type] = amount_limit
    
    def push(self, message):
        message.push_time = time.time()
        message.id = self.next_message_id
        self.next_message_id += 1
        t = message.message_type
        if not t in self.messages_by_type:
            self.messages_by_type[t] = []

        self.messages_by_type[t].append(message)
        if t in self.type_limits:
            if len(self.messages_by_type[t]) > self.type_limits[t]:
                self.messages_by_type[t].pop(0)

    def get_messages(self):
        now = time.time()
        messages = []
        for t in self.messages_by_type:
            self.messages_by_type[t] = self.remove_old(self.messages_by_type[t])

        for msgs in self.messages_by_type.values():
            messages += msgs
        return messages

    def remove_old(self, messages):
        now = time.time()
        return [
                message for message in messages
                if not self.is_too_old(message, now)
        ]
    
    def is_too_old(self, message, now):
        if not isinstance(message, HasTimeLimit):
            return False
        else:
            return now - message.push_time > message.get_time_to_live()

