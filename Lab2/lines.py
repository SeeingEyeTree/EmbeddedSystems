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
            sense.set_pixel(c, r, (0,0,0))


for i in range(7):
    x = i
    for j in range(7):
        y = j
        slope = (y_end - y) / (x_end - x) if (x_end - x) != 0 else 0
        color_val = min(255, int(abs(50 * slope)))
        for k in range(7 - x + 1):
            px = x + k
            py = int(y + k * slope)
            if 0 <= py <= 7:
                hat.set_pixel(px, py, (color_val, int(color_val/2), int(color_val/4)))
        time.sleep(0.2)
        clear_sensehat()
        