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
    for dx in [0, 1]:
        for dy in [0, 1]:
            if dx == 0 and dy == 0 or (dx == 1 and dy == 1):
                continue
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                adjacent_pixels.append((new_x, new_y))
    return adjacent_pixels

if __name__ == "__main__":

    pixels = [[0,0]]
    visited = [pixels[0]]
    i = 0
    while True:
        color =r
        if i % 4 == 0:
            color = r
        elif i % 4 == 1:
            color = yellow
        elif i % 4 == 2:
            color = g
        elif i % 4 == 3:
            color = b

        i += 1
        clear_sensehat()
        for x, y in pixels:
            sense.set_pixel(x, y, color)
            visited.append((x, y))

        time.sleep(0.3)

        next_pixels = []
        for x, y in pixels:
            for p in get_adjacent_pixels(x, y):
                if p not in visited:
                    next_pixels.append(p)
        if any(p == (7, 7) for p in next_pixels):
            # reset the pixels to start over
            pixels = [[0, 0]] # double just to make sure 
            next_pixels = [(0,0)]
            visited = [pixels[0]]
        pixels = next_pixels