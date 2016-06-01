from numpy import *
import math
from linalg import *

class LaticeRenderer(object):
    def __init__(self):
        self._center = [0, 0]
        self._rotation = 0.0
        self._scale = 1
        self._func = lambda x, y: (0, 0, 0, 0)

    def set_center(self, center):
        self._center = center

    def set_rotation(self, rotation):
        self._rotation = rotation

    def set_scale(self, scale):
        self._scale = scale

    def move(self, v):
        vec2_add(self._center, v)

    def rotate(self, a):
        self._rotation += a

    def scale(self, s):
        self._scale *= s

    def set_func(self, func):
        self._func = func

    def render(self, image):
        asn = math.sin(self._rotation)
        acs = math.cos(self._rotation)

        image_dim = image.get_dim()
        scale = (float(self._scale), float(image_dim[1]) / image_dim[0] * self._scale)

        start = vec2_sub(self._center, vec2_rotate(vec2_divs(scale, 2), asn, acs))

        step_x = vec2_muls(vec2_rotate((1, 0), asn, acs), scale[0] / image_dim[0])
        step_y = vec2_muls(vec2_rotate((0, 1), asn, acs), scale[1] / image_dim[1])

        for x in xrange(image_dim[0]):
            for y in xrange(image_dim[1]):
                xy = vec2_add3(start, vec2_muls(step_x, x), vec2_muls(step_y, y))

                image[x, y] = self._func(xy[0], xy[1])
