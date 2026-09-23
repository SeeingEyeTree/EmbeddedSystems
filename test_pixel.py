from sense_hat import SenseHat
import time
from image_to_grid import frame_to_grid
sense = SenseHat()

while True:
        sense.set_pixel(0, 2, (0, 0, 255))
        time.sleep(1)
        sense.set_pixel(7, 4, (255, 0, 0))
        time.sleep(1)