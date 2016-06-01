import math
from graphics import *
from random import randint, uniform
from scenes.LaticeRenderer import LaticeRenderer

class FunctionScene2(object):
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
        self._dropParam = [((0.3,-0.4),1,30),((0.1,0.2),1,30)]
        self._ptAparam = [0.5, uniform(0.5, 2.0), uniform(0, 10)]
        self._ptBparam = [uniform(0.05, 0.3), uniform(0.5, 2.0), uniform(0, 10)]
        self._time = 0

        self._rotate_speed = uniform(-1, 1);
        self._scale_amp = uniform(0.01, 0.1);
        self._scale_freq = uniform(8, 16);
        self._hue = uniform(0.0, 1.0);
        self._hue_speed = uniform(0.2, 0.7);

        fill_image(self._result_image, hsia_to_color4(uniform(0, 1), uniform(0.3, 0.5), uniform(0.3, 0.5), 1))


    def _func(self,x,y):

        t= (x-ptBx)/(ptAx-ptBx)
        if (abs(y-ptAy*t -ptBy*(1-t))<0.01) and t>0 and t<1:
            s= 1
        else:
            s=0
        return hsia_to_color4(self._hue, 1, s, 1)



    def update(self, dt):
        #self._renderer.rotate(self._rotate_speed * dt)
        #self._renderer.set_scale(self._scale_amp * math.sin(self._time / self._scale_freq) + 1)

        self._hue += self._hue_speed * dt

        self._time += 3*dt
        ptAAmp,ptAfreq,ptAstart = self._ptAparam
        ptBAmp,ptBfreq,ptBstart = self._ptBparam
        ptAx = ptAAmp*math.cos(ptAfreq*self._time+ptAstart)
        ptAy = ptAAmp*math.sin(ptAfreq*self._time+ptAstart)
        ptBx = ptBAmp*math.cos(ptBfreq*self._time+ptBstart)
        ptBy = ptBAmp*math.sin(ptBfreq*self._time+ptBstart)

        #self._renderer.render(self._image)
        #downscale(self._result_image, self._image, 2)
        #for x in range(30):
        #    for y in range(30):
        #        self._result_image[x,y]=hsia_to_color4(0,0,0,1)
        for i in range(30):
            x = int(ptAx*i+ptBx*(30-i)) +15
            y = int(ptAy*i+ptBy*(30-i)) +15
            self._result_image[x,y]=hsia_to_color4(self._hue,1,1,1)
        return self._result_image

