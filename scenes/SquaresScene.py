from sig import Timer
from graphics import *
from random import uniform, choice, randint


class SquaresScene(object):
    def __init__(self):
        self._frame = Sprite((30, 30))
        self._timer = Timer(self._tick)
        self._timer.set_period(0.1)

    def poke(self):
        fill_image(self._frame, (0, 0, 0, 1))
        self._timer.set_period(uniform(0.08, 0.3))

        self._size = choice([5, 6, 10, 15])
        self._num = 30 / self._size
        self._num_per_tick = randint(1, 8)

    def _tick(self):
        for i in range(self._num_per_tick):
            self._draw_sqaure()

    def _draw_sqaure(self):
        sx = randint(0, self._num - 1)
        sy = randint(0, self._num - 1)

        xo = sx * self._size
        yo = sy * self._size

        hue = uniform(0, 1)
        sat = uniform(0.5, 1)
        inten = uniform(0.4, 1)
        for x in range(self._size):
            for y in range(self._size):
                self._frame[xo + x, yo + y] = hsia_to_color4(hue, sat, inten, 1)

    def update(self, dt):
        self._timer.update(dt)

        return self._frame