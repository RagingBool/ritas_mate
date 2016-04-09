import math
from mathutils import *
from os import path, listdir
from PIL import Image


class Sprite(object):
    def __init__(self, dim):
        self._dim = dim
        self._data = [(0, 0, 0, 0)] * (dim[0] * dim[1])

    def get_dim(self):
        return self._dim

    def set_data(self, data):
        self._data = data;

    def __getitem__(self, pos):
        return self._data[self._to_index(pos)]

    def __setitem__(self, pos, value):
        self._data[self._to_index(pos)] = value

    def _to_index(self, pos):
        return pos[1] * self._dim[0] + pos[0]


def load_image(image_path):
    bitmap = Image.open(image_path)
    image = Sprite(bitmap.size)

    pal = bitmap.getpalette()
    if pal:
        pallette = [color4_from_8bit(pal[i * 3:(i + 1) * 3]) for i in range(int(len(pal) / 3))]
        image.set_data([pallette[x] for x in list(bitmap.getdata())])
    else:
        image.set_data(list([color4_from_8bit(x) for x in bitmap.getdata()]))

    return image


def load_images(dir_path):
    files = listdir(dir_path)
    files.sort()
    return [load_image(path.join(dir_path, x)) for x in files if x[0] != "."]


def fill_image(image, c):
    image.set_data([c] * (image.get_dim()[0] * image.get_dim()[1]))


def blit(dest, src, pos, alpha=1.0):
    for y in range(src.get_dim()[1]):
        for x in range(src.get_dim()[0]):
            dx = pos[0] + x
            dy = pos[1] + y

            if (0 <= dx < dest.get_dim()[0]) and (0 <= dy < dest.get_dim()[1]):
                dest[(dx, dy)] = blend(dest[(dx, dy)], src[(x, y)], alpha)


def blend(c1, c2, alpha):
    k2 = c2[3] * alpha
    k1 = (1.0 - k2) * c1[3]

    return (k1 * c1[0] + k2 * c2[0],
            k1 * c1[1] + k2 * c2[1],
            k1 * c1[2] + k2 * c2[2],
            k1 + k2)


def downscale(dest, src, super_res):
    subpixels = super_res * super_res
    for y in range(dest.get_dim()[1]):
        for x in range(dest.get_dim()[0]):
            avg_color = [0, 0, 0, 0]
            for px in xrange(super_res):
                for py in xrange(super_res):
                    c = src[(x * super_res + px, y * super_res + py)]
                    avg_color[0] += c[0]
                    avg_color[1] += c[1]
                    avg_color[2] += c[2]
                    avg_color[3] += c[3]
            avg_color[0] /= subpixels
            avg_color[1] /= subpixels
            avg_color[2] /= subpixels
            avg_color[3] /= subpixels

            dest[(x, y)] = avg_color


def apply_gamma(x, gamma):
    return clip(x) ** gamma


def translate(image):
    numLEDs = 1024
    pixels = [(0,0,0)] * numLEDs
    i = 0
    delta = 1
    for y in range(image.get_dim()[1]):
        for x in range(image.get_dim()[0]):
            c = [apply_gamma(x, 1.2) for x in image[(x, y)]]
            pixels[i] = color4_to_8bit(c)[0:3]
            i += delta
        delta *= -1
        if delta == -1:
            i += 29
        else:
            i += 35
    return pixels


def render(client, image):
    client.put_pixels(translate(image))


# Based on a post by Brian Neltner: http://blog.saikoled.com/post/43693602826/why-every-led-light-should-be-using-hsi
def hsia_to_color4(hue, saturation, intensity, a):
    nh = wrap_unit(hue)
    cs = clip(saturation)
    ci = clip(intensity)

    if nh < third:
        rad = tau * nh
        r = math.cos(rad) / math.cos(pi_div_3 - rad)
        c1 = ci * (1 + cs * r)
        c2 = ci * (1 + cs * (1 - r))
        c3 = ci * (1 - cs)
    elif nh < two_thirds:
        rad = tau * (nh - third)
        r = math.cos(rad) / math.cos(pi_div_3 - rad)
        c2 = ci * (1 + cs * r)
        c3 = ci * (1 + cs * (1 - r))
        c1 = ci * (1 - cs)
    else:
        rad = tau * (nh - two_thirds)
        r = math.cos(rad) / math.cos(pi_div_3 - rad)
        c3 = ci * (1 + cs * r)
        c1 = ci * (1 + cs * (1 - r))
        c2 = ci * (1 - cs)

    return c1, c2, c3, a


def color4_to_hsia(c1, c2, c3, a):
    cc1 = clip(c1)
    cc2 = clip(c2)
    cc3 = clip(c3)

    minc = min(cc1, cc2, cc3)
    maxc = max(cc1, cc2, cc3)

    if minc != maxc:
        nr = cc1 / maxc
        ng = cc2 / maxc
        nb = cc3 / maxc

        hue_norm_acos = math.acos(
            (0.5 * (2 * nr - ng - nb)) /
            math.sqrt((nr - ng) * (nr - ng) + (nr - nb) * (ng - nb))) / tau

        hue = hue_norm_acos if (nb <= ng) else 1 - hue_norm_acos

        intensity = (cc1 + cc2 + cc3) / 3
        saturation = 1 - minc / intensity
    else:
        hue = 0
        saturation = 0
        intensity = minc

    return hue, saturation, intensity, a


def color4_from_8bit(c):
    return clip(c[0] / 255.0),\
           clip(c[1] / 255.0),\
           clip(c[2] / 255.0),\
           clip(c[3] / 255.0) if len(c) == 4 else 1.0


def color4_to_8bit(c):
    return int(clip(c[0]) * 255.0),\
           int(clip(c[1]) * 255.0),\
           int(clip(c[2]) * 255.0),\
           int(clip(c[3]) * 255.0)
