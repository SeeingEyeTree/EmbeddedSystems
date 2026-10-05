from sense_hat import SenseHat
import time
o = (255, 165, 0)
r = (255, 0, 0)          # red
yellow = (255, 255, 0)        # yellow
g = (0, 128, 0)          # green
b = (0, 0, 255)          # blue
v = (128, 0, 128)        # violet
k = (0, 0, 0)            # nothing
sense = SenseHat()

def clear_sensehat():
    for r in range(8):
        for c in range(8):
            sense.set_pixel(c, r, (0,0,0))

def get_adjacent_pixels(x, y):
    adjacent_pixels = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                adjacent_pixels.append((new_x, new_y))
    return adjacent_pixels

if __name__ == "__main__":
    clear_sensehat()
    pixels = [[0,0]]
    visited = [pixels[0]]
    while True:
        for pixel in pixels:
            x, y = pixel
            sense.set_pixel(x, y, r)
            visited.append(pixel)
            pixels.append(get_adjacent_pixels(pixel[0], pixel[1]))
        
