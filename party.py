from sig import Timer
from graphics import render
from opc import Client
from scenes.SpritesScene import SpritesScene
from scenes.MandelScene import MandelScene
import random

class Party(object):
    def __init__(self):
        self._client = Client('localhost:7890')
        self._scenes = [
            SpritesScene(),
            MandelScene(),
        ]
        self._timer = Timer(self._switch)
        self._timer.set_period(2.0)
        self._switch()

    def _switch(self):
        self._scene = random.choice(self._scenes)

    def update(self, dt):
        self._timer.update(dt)
        frame = self._scene.update(dt)

        render(self._client, frame)
