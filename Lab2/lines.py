from image_to_grid import display_grid
import time
from sense_hat import SenseHat
hat = SenseHat()
x_end = 7
y_end = 7


def clear_sensehat():
    from sense_hat import SenseHat
    sense = SenseHat()
    for r in range(8):
        for c in range(8):
            sense.set_pixel(c, r, 0)


for i in range(7):
    x = i
    for j in range(7):
        y = j
        slope = (y_end - y) / (x_end - x) if (x_end - x) != 0 else None
        hat.set_pixel(x, y, (int(10* slope), 0, 50))
        for k in range(7 - x):
            hat.set_pixel(x + k, int(y + slope), (int(10* slope), 0, 50))
        time.sleep(0.2)
        clear_sensehat()
        