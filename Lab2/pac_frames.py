
import time
from image_to_grid import display_grid, print_pixel_art

y = (255, 255, 0)
k = (0, 0, 0)
cy = (3, 169, 244)
r = (213, 0, 0)
pk = (233, 30, 99)
o = (245, 124, 0)
w = (255, 255, 255)
b = (63, 81, 181)
am = (255, 193, 7)

frame_0 = [
    [k, k, y, y, y, y, y, k],
    [k, y, y, y, y, y, y, y],
    [y, y, y, k, y, y, y, k],
    [y, y, y, y, y, y, k, k],
    [y, y, y, y, y, k, k, k],
    [y, y, y, y, y, y, k, k],
    [y, y, y, y, y, y, y, k],
    [k, y, y, y, y, y, y, y],
]

frame_1 = [
    [k, k, y, y, y, y, k, k],
    [k, y, y, y, y, y, y, k],
    [y, y, y, k, y, y, y, y],
    [y, y, y, y, y, y, y, y],
    [y, y, y, y, y, am, am, am],
    [y, y, y, y, y, y, y, y],
    [y, y, y, y, y, y, y, k],
    [k, y, y, y, y, y, k, k],
]

frame_2 = [
    [k, k, y, y, y, y, y, k],
    [k, y, y, y, y, y, y, y],
    [y, y, y, k, y, y, y, k],
    [y, y, y, y, y, y, k, k],
    [y, y, y, y, y, k, k, k],
    [y, y, y, y, y, y, k, k],
    [y, y, y, y, y, y, y, k],
    [k, y, y, y, y, y, y, y],
]

frame_3 = [
    [k, k, y, y, y, y, k, k],
    [k, y, y, y, y, y, y, k],
    [y, y, y, k, y, y, y, y],
    [y, y, y, y, y, y, y, y],
    [y, y, y, y, y, am, am, am],
    [y, y, y, y, y, y, y, y],
    [y, y, y, y, y, y, y, k],
    [k, y, y, y, y, y, k, k],
]

frame_4 = [
    [k, k, k, cy, cy, cy, k, k],
    [k, k, cy, cy, cy, cy, cy, k],
    [k, cy, w, w, cy, w, w, cy],
    [k, cy, w, b, cy, w, b, cy],
    [k, cy, cy, cy, cy, cy, cy, cy],
    [k, cy, cy, cy, cy, cy, cy, cy],
    [k, cy, cy, cy, cy, cy, cy, cy],
    [k, cy, k, cy, k, cy, k, cy],
]

frame_5 = [
    [k, k, k, r, r, r, k, k],
    [k, k, r, r, r, r, r, k],
    [k, r, w, w, r, w, w, r],
    [k, r, w, b, r, w, b, r],
    [k, r, r, r, r, r, r, r],
    [k, r, r, r, r, r, r, r],
    [k, r, r, r, r, r, r, r],
    [k, r, k, r, k, r, k, r],
]

frame_6 = [
    [k, k, k, pk, pk, pk, k, k],
    [k, k, pk, pk, pk, pk, pk, k],
    [k, pk, w, w, pk, w, w, pk],
    [k, pk, w, b, pk, w, b, pk],
    [k, pk, pk, pk, pk, pk, pk, pk],
    [k, pk, pk, pk, pk, pk, pk, pk],
    [k, pk, pk, pk, pk, pk, pk, pk],
    [k, pk, k, pk, k, pk, k, pk],
]

frame_7 = [
    [k, k, k, o, o, o, k, k],
    [k, k, o, o, o, o, o, k],
    [k, o, w, w, o, w, w, o],
    [k, o, w, b, o, w, b, o],
    [k, o, o, o, o, o, o, o],
    [k, o, o, o, o, o, o, o],
    [k, o, o, o, o, o, o, o],
    [k, o, k, o, k, o, k, o],
]

frames = [frame_0, frame_1, frame_2, frame_3, frame_4, frame_5, frame_6, frame_7]

if __name__ == "__main__":
    while True:
        for frame in frames:
            display_grid(frame)
            time.sleep(0.15)
