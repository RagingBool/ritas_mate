from graphics import *
from random import randint, uniform


class SpritesScene(object):
    def __init__(self):
        self._acc_time = 0

        self._images = load_images("sprites")
        self._background = Sprite((30, 30))
        fill_image(self._background, (1, 0, 0, 1))
        self._frame = Sprite((30, 30))
        self._last_image_change = 0
        self._image_change_time = 0.5
        self._hues = [uniform(0, 1) for i in range(4)]
        self._count = 100
        self._hues_vel = []
        self._saturation = 0
        self._intensity = 0
        self._image = None
        self._alpha = 0
        self._reset = True

    def update(self, dt):
        self._acc_time += dt

        if self._acc_time > self._image_change_time or self._reset:
            if self._reset:
                self._acc_time = 0
                self._reset = False

            self._acc_time -= self._image_change_time
            self._image = self._images[randint(0, len(self._images) - 1)]
            self._alpha = uniform(0.9, 0.97)

            self._count += 1
            if self._count > 10:
                self._hues_vel = [uniform(-0.5, 0.5) for i in range(4)]
                self._saturation = uniform(0.5, 1)
                self._intensity = uniform(0.5, 1)
                self._count = 0

        self._hues = [wrap_unit(self._hues[i] + self._hues_vel[i] * dt) for i in range(4)]
        render_corner_gradient(self._background, self._hues, self._saturation, self._intensity)

        blit(self._frame, self._background, (0, 0))
        blit_centered(self._frame, self._image, self._alpha)

        return self._frame


def render_corner_gradient(image, hues, saturation, intensity):
    dim = image.get_dim()
    #corners = [(0, 0), (dim[0] - 1, 0), (0, dim[1] - 1), (dim[0] - 1, dim[1] - 1)]
    for x in range(dim[0]):
        for y in range(dim[1]):
            xn = float(x) / (dim[0] - 1)
            yn = float(y) / (dim[1] - 1)
            intr_top = interp(hues[0], hues[1], xn)
            intr_bottom = interp(hues[2], hues[3], xn)
            intr = interp(intr_top, intr_bottom, yn)

            #p = (x, y)
            #dists = [dist2(p, c) for c in corners]
            #print dists
            #print interp_dists(dists, hues)
            #intr = interp_dists(dists, hues)
            image[x, y] = hsia_to_color4(intr, saturation, intensity, 1)


def interp_dists(dists, hues):
    m = max(dists)
    s = float(sum([m - x for x in dists]))
    dists_norm = [x / s for x in dists]

    result = 0
    for i in range(len(dists)):
        result += hues[i] * dists_norm[i]

    return result


def interp(a, b, x):
    return a * (1 - x) + b * x


def dist2(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return dx * dx + dy * dy


def blit_centered(dest, src, alpha):
    x = (dest.get_dim()[0] - src.get_dim()[0]) / 2
    y = (dest.get_dim()[1] - src.get_dim()[1]) / 2
    blit(dest, src, (x, y), alpha)
