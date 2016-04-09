from graphics import *
from opc import Client
from time import sleep
from random import randint, uniform
import time


def main():
    client = Client('localhost:7890')
    images = load_images("sprites")

    background = Sprite((30, 30))
    fill_image(background, (1, 0, 0, 1))
    frame = Sprite((30, 30))
    last_image_change = 0
    image_change_time = 0.5
    hues = [uniform(0, 1) for i in range(4)]
    count = 100
    while True:
        cur_time = time.time()
        if cur_time > last_image_change + image_change_time:
            last_image_change = cur_time
            image = images[randint(0, len(images) - 1)]
            alpha = uniform(0.9, 0.97)

            count += 1
            if count > 10:
                hues_vel = [uniform(-0.01, 0.01) for i in range(4)]
                saturation = uniform(0.5, 1)
                intensity = uniform(0.5, 1)
                count = 0

        hues = [wrap_unit(hues[i] + hues_vel[i]) for i in range(4)]
        render_corner_gradient(background, hues, saturation, intensity)

        blit(frame, background, (0, 0))
        blit_centered(frame, image, alpha)
        render(client, frame)
        sleep(0.02)


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

main()
