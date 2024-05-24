import time


class Value:
    def __init__(self, sensorvalidity: int = None):
        self._value = None
        self._sensorvalidity = sensorvalidity
        self._last_set = time.monotonic()
        self.topic_state = None

    def set_value(self, temp):
        self._last_set = time.monotonic()
        self._value = temp

    def set_time(self, time_value):
        if time_value - self._last_set > self._sensorvalidity:
            self._value = None

    def value(self):
        return self._value

    def publish_state(self):
        # print("TODO")
        return ()

    def do_subscribes(self):
        return ()
