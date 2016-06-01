import math
from graphics import *
from random import randint, uniform
from scenes.LaticeRenderer import LaticeRenderer

class FunctionScene(object):
    def __init__(self):
        self._image = Sprite((60, 60))
        self._result_image = Sprite((30, 30))
        self._renderer = LaticeRenderer()
        self.poke()

#    def _func(self, x, y):
#        hue = math.sin((x * x + y * y) ** 0.5)
#        return hsia_to_color4(hue, 1, 1, 1)

    def poke(self):
        self._renderer.set_center((0, 0))
        self._renderer.set_rotation(0)
        self._renderer.set_scale(1.0)
        self._renderer.set_func(self._func)
        #self._dropParam = [((0.3,-0.4),1,30)]#,((0.1,0.2),1,30)]

        self._dropParam = []
        bloops = randint(1, 3)
        for i in range(bloops):
            self._dropParam.append(((uniform(-1, 1), uniform(-1, 1)), uniform(0.5, 1), uniform(10, 30)))

        self._time = 0

        self._rotate_speed = uniform(-1, 1);
        self._scale_amp = uniform(0.01, 0.1);
        self._scale_freq = uniform(8, 16);
        self._hue1 = uniform(0.0, 1.0);
        self._hue2 = self._hue1 + uniform(0.15, 0.35)
        self._low_int = uniform(0.1, 0.4)


    def _func(self,x,y):
        maxamp = sum([z[1] for z in self._dropParam])
        s = 0
        for (x0,y0),A,phi in self._dropParam:
            r = ((x-x0)**2+(y-y0)**2)**0.5
            s += A*(math.sin(r*phi-self._time))
        s = (s+maxamp)/(4.*maxamp)

        hue = interpolate(self._hue1, self._hue2, s)
        intensity = interpolate(self._low_int, 1, s)

        return hsia_to_color4(hue, 1, intensity, 1)



    def update(self, dt):
        self._renderer.rotate(self._rotate_speed * dt)
        self._renderer.set_scale(self._scale_amp * math.sin(self._time / self._scale_freq) + 1)

        self._time += 4*dt
        self._renderer.render(self._image)
        downscale(self._result_image, self._image, 2)

        return self._result_image

