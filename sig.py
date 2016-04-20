class Timer(object):
    def __init__(self, event):
        self._period = 1.0
        self._event = event
        self._acc = 0

    def set_period(self, period):
        self._period = period

    def update(self, dt):
        self._acc += dt

        if self._acc > self._period:
            self._acc = 0
            self._event()
