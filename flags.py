# Color definitions as RGB tuples
t = (91, 206, 250)       # trans light blue
p = (245, 169, 184)      # trans pink
w = (255, 255, 255)      # white
r = (255, 0, 0)          # red
o = (255, 165, 0)        # orange
y = (255, 255, 0)        # yellow
g = (0, 128, 0)          # green
b = (0, 0, 255)          # blue
v = (128, 0, 128)        # violet/purple
k = (0, 0, 0)            # black
br = (139, 69, 19)       # brown
dr = (210, 0, 0)         # dark red/lesbian flag
gy = (128, 128, 128)     # grey
from image_to_pixelart import display_grid
import time

# Trans Flag (5 stripes)
trans_flag = [
    [t] * 8,
    [t] * 8,
    [p] * 8,
    [w] * 8,
    [p] * 8,
    [p] * 8,
    [t] * 8,
    [k] * 8,
]

# Rainbow Pride Flag (6 stripes)
rainbow_flag = [
    [r] * 8,
    [o] * 8,
    [y] * 8,
    [g] * 8,
    [b] * 8,
    [v] * 8,
    [k] * 8,
    [k] * 8,
]

# Lesbian Flag (5 stripes)
lesbian_flag = [
    [o] * 8,
    [o] * 8,
    [w] * 8,
    [w] * 8,
    [w] * 8,
    [p] * 8,
    [dr] * 8,
    [k] * 8,
]

# Asexual Flag (4 stripes)
asexual_flag = [
    [k] * 8,
    [k] * 8,
    [gy] * 8,
    [gy] * 8,
    [w] * 8,
    [w] * 8,
    [v] * 8,
    [v] * 8,
]

# Nonbinary Flag (4 stripes)
nonbinary_flag = [
    [y] * 8,
    [y] * 8,
    [w] * 8,
    [w] * 8,
    [v] * 8,
    [v] * 8,
    [k] * 8,
    [k] * 8,
]

# Progress Pride Flag (chevron + rainbow)
progress_flag = [
    [t, t, r, r, r, r, r, r],
    [t, t, o, o, o, o, o, o],
    [p, p, y, y, y, y, y, y],
    [w, w, g, g, g, g, g, g],
    [br, br, b, b, b, b, b, b],
    [k, k, v, v, v, v, v, v],
    [k, k, k, k, k, k, k, k],
    [k, k, k, k, k, k, k, k],
]


if __name__ == "__main__":
    while True:
        display_grid(trans_flag)
        time.sleep(1)
        display_grid(rainbow_flag)
        time.sleep(1)
        display_grid(lesbian_flag)
        time.sleep(1)
        display_grid(asexual_flag)
        time.sleep(1)
        display_grid(nonbinary_flag)
        time.sleep(1)
        display_grid(progress_flag)
        time.sleep(1)