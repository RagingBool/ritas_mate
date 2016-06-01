import abc
from linalg import *
from graphics import *
from ComponentManager import ComponentManager


class SceneBase(object):
    def __init__(self, dim, super_res=False):
        self._super_res = super_res
        self._components = ComponentManager()

        if self._super_res:
            self._frame = Sprite(vec2_muls(dim, 2))
            self._result = Sprite(dim)
        else:
            self._frame = Sprite(dim)
            self._result = self._frame

    @property
    def super_res(self):
        return self._super_res

    @property
    def components(self):
        return self._components

    @property
    def frame(self):
        return self._frame

    def poke(self):
        self.components.poke()
        self.poke_this()

    def update(self, dt):
        self.components.update(dt)
        self.update_this(dt)

        if self._super_res:
            downscale(self._result, self._frame, 2)

        return self._result

    @abc.abstractmethod
    def poke_this(self):
        pass

    @abc.abstractmethod
    def update_this(self, dt):
        pass
