import gamegridp
from collections import defaultdict

class Observer:
    def listen(self, event, data):
        pass


class EventManager:
    def __init__(self):
        self._observers = defaultdict(list)

    def register_observer(self, observer, event):
        self._observers[event].append(observer)

    def notify_observers(self, event, data):
        for observer in self._observers[event]:
            observer.listen(event, data)

