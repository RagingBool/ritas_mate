import math

class Timer(object):
    def __init__(self, event):
        self._period = 1.0
        self._event = event
        self._acc = 0

    def set_period(self, period):
        self._period = period
        self._acc = 0

    def update(self, dt):
        self._acc += dt

        if self._acc > self._period:
            self._acc -= self._period
            self._event()


class PhaseGenerator(object):
    def __init__(self):
        self._freq = 1.0
        self._phase = 0.0;

    def poke(self):
        pass

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, freq):
        self._freq = freq

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase):
        self._phase = phase

    def reset(self):
        self._phase = 0

    def update(self, dt):
        adv_phase = self._phase + (dt * self._freq)

        self._phase = adv_phase if adv_phase < 1 else adv_phase - 1.0


class Oscillator(object):
    SAW_UP = 0
    SAW_DOWN = 1
    SQUARE = 2
    TRIANGLE = 3
    SIN = 4

    def __init__(self):
        self._phase_gen = PhaseGenerator()
        self._function_type = Oscillator.SAW_DOWN
        self._value = 0.0

    @property
    def function_type(self):
        return self._function_type

    @function_type.setter
    def function_type(self, function_type):
        self._function_type = function_type

    @property
    def freq(self):
        return self._phase_gen.freq

    @freq.setter
    def freq(self, freq):
        self._phase_gen.freq = freq

    @property
    def period(self):
        return 1.0 / self._phase_gen.freq

    @period.setter
    def period(self, period):
        self._phase_gen.freq = 1.0 / period

    @property
    def phase(self):
        return self._phase_gen.phase

    @phase.setter
    def phase(self, phase):
        self._phase_gen.phase = phase

    @property
    def value(self):
        return self._value

    def reset(self):
        self._phase_gen.reset()

    def update(self, dt):
        self._phase_gen.update(dt)
        phase = self._phase_gen.phase
        func = self._function_type

        if func == Oscillator.SAW_UP:
            self._value = phase
        elif func == Oscillator.SAW_DOWN:
            self._value = 1.0 - phase
        elif func == Oscillator.SQUARE:
            self._value = 0.0 if phase < 0.5 else 1.0
        elif func == Oscillator.TRIANGLE:
            double_phase = phase * 2
            self._value = double_phase if double_phase <= 1.0 else 2.0 - double_phase
        elif func == Oscillator.SIN:
            self._value = math.sin(phase * math.pi * 2) / 2 + 0.5
        else:
            self._value = 0.0
