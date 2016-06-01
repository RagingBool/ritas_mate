from sig import Timer
from graphics import render
from opc import Client
from scenes.SpritesScene import SpritesScene
from scenes.MandelScene import MandelScene
from scenes.FunctionScene import FunctionScene
from scenes.FunctionScene2 import FunctionScene2
from scenes.SquaresScene import SquaresScene
import random

class Party(object):
    def __init__(self):
        self._client = Client('localhost:7890')
        self._scenes = [
            SpritesScene(),
            MandelScene(),
            FunctionScene(),
            FunctionScene2(),
            SquaresScene(),
        ]
        self._timer = Timer(self._switch)
        self._timer.set_period(10.0)
        self._switch()

    def _switch(self):
        self._scene = random.choice(self._scenes)
        self._scene.poke()

    def update(self, dt):
        self._timer.update(dt)
        frame = self._scene.update(dt)

        render(self._client, frame)
