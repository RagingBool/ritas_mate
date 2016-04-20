from graphics import render
from opc import Client
from scenes.SpritesScene import SpritesScene


class Party(object):
    def __init__(self):
        self._client = Client('localhost:7890')
        self._scene = SpritesScene()

    def update(self, dt):
        frame = self._scene.update(dt)

        render(self._client, frame)
