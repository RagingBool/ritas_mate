from time import sleep
from numpy import *
from graphics import *
from opc import Client
from random import randint, uniform
from mathutils import *
import math
from linalg import *


def main():
    client = Client('localhost:7890')
    super_res = 2

    image = Sprite((30 * super_res, 30 * super_res))
    background = Sprite((30, 30))
    points = [
        #(( 0.3750001200618655, -0.2166393884377127), 100),
        #((-0.13856524454488, -0.64935990748190), 100),
        ((-0.75, 0.1), 200),
        ((0.275, 0), 200),
        ((-0.088, 0.654), 250),
        ((0.274, 0.482), 200),
        ((-0.1002, 0.8383), 220),
        #((-1.36, 0.005 ), 130),
        #((-1.75, 0), 200),
        ((-1.6, 0), 600),
        ((-1.74, 0), 600),
        ((-1.108, 0.230), 200),
        ((-0.1592, -1.0317), 130),
    ]

    while True:
        scale = 10
        point = points[randint(0, len(points) - 1)]
        cs = uniform(1.5, 6.5)
        pal = randint(0, 3)
        frames = point[1]
        out_frame = frames / 2
        zoom = uniform(0.86, 0.92)
        print point
        angle = uniform(0, math.pi * 2)
        rotate_speed = uniform(-0.04, 0.04)
        for i in xrange(frames):
            render_mandelbrot(image, point[0], scale, angle, cs, pal, 150)
            downscale(background, image, super_res)

            render(client, background)
            sleep(0.01)

            if i < out_frame:
                scale *= zoom
            else:
                scale /= zoom
            angle += rotate_speed


def render_mandelbrot(image, center, x_scale, angle, cs, pal, maxiter):
    asn = math.sin(angle)
    acs = math.cos(angle)

    image_dim = image.get_dim()
    scale = (float(x_scale), float(image_dim[1]) / image_dim[0] * x_scale)

    start = vec2_sub(center, vec2_rotate(vec2_divs(scale, 2), asn, acs))

    step_x = vec2_muls(vec2_rotate((1, 0), asn, acs), scale[0] / image_dim[0])
    step_y = vec2_muls(vec2_rotate((0, 1), asn, acs), scale[1] / image_dim[1])

    for x in xrange(image_dim[0]):
        for y in xrange(image_dim[1]):
            z = vec2_add3(start, vec2_muls(step_x, x), vec2_muls(step_y, y))

            image[x, y] = to_color(mandelbrot(complex(z[0], z[1]), maxiter), cs, pal, maxiter)


def to_color(val, cs, pal, maxiter):
    if val == 0 or val == maxiter:
        return 0, 0, 0, 0
        #return (cs * 30) % 256, (cs * 50) % 256, (cs * 130) % 256

    #xxvall = math.log(val, 1.2)
    vall = val

    cols = wrap_unit(0.5 + vall * 0.04 * cs),\
           wrap_unit(1 - vall * 0.021 * cs),\
           wrap_unit(vall * 0.003 * cs),\

    if pal == 0:
        return cols[0], cols[1], cols[2], 1.0
    elif pal == 1:
        return cols[1], cols[0], cols[2], 1.0
    elif pal == 1:
        return cols[0], cols[2], cols[1], 1.0
    else:
        return cols[2], cols[1], cols[0], 1.0


def mandelbrot(z, maxiter):
    c = z

    for n in xrange(maxiter):
        if abs(z) > 2:
            return n
        z = z * z + c

    return maxiter


main()
