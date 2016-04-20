import time
from party import Party


def main():
    p = Party()

    last_t = time.time()
    frame_time = 1.0 / 60
    while True:
        cur_t = time.time()
        p.update(cur_t - last_t)
        update_t = time.time() - cur_t
        sleep_t = frame_time - update_t
        last_t = cur_t

        if sleep_t > 0:
            time.sleep(sleep_t)


main()