import argparse
import sys
import time
import cv2
from colorama import just_fix_windows_console

just_fix_windows_console()

RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CURSOR_HOME = "\033[H"
CLEAR_SCREEN = "\033[2J"


def truecolor_bg(r, g, b):
    """ANSI escape code that sets the background to an exact RGB color."""
    return f"\033[48;2;{r};{g};{b}m"


def frame_to_grid(frame_bgr, cols, rows):
    """Take a raw BGR frame (as OpenCV gives you) and reduce it to a
    cols x rows grid of (r, g, b) tuples. Shared by image and video paths."""
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Downscaling with INTER_AREA box-filters (averages) each source block
    # into a single output pixel -- this IS the "average each cell" step.
    small = cv2.resize(frame_rgb, (cols, rows), interpolation=cv2.INTER_AREA)

    return [[tuple(int(c) for c in pixel) for pixel in row] for row in small]


def image_to_grid(path, cols, rows):
    """Load an image and reduce it to a cols x rows grid of (r, g, b) tuples."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return frame_to_grid(img, cols, rows)


def grid_to_lines(grid, pixel="  "):
    """Render a grid to a list of printable strings (one per row)."""
    return [
        "".join(truecolor_bg(*rgb) + pixel for rgb in row) + RESET
        for row in grid
    ]


def print_pixel_art(grid, pixel="  "):
    """Print one grid as terminal pixel art."""
    for line in grid_to_lines(grid, pixel):
        print(line)


def display_grid(grid):
    """Display the grid on the Sense HAT LED matrix."""
    from sense_hat import SenseHat
    sense = SenseHat()
    for r, row in enumerate(grid):
        for c, rgb in enumerate(row):
            sense.set_pixel(c, r, rgb)


def video_to_grids(path, cols, rows):
    """Load every video frame as a list of RGB grids."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {path}")
    try:
        grids = []
        while True:
            ret, frame = cap.read()
            if not ret:
                return grids
            grids.append(frame_to_grid(frame, cols, rows))
    finally:
        cap.release()


def display_grids_terminal(grids, fps=30.0, pixel="  ", loop=False):
    """Play a sequence of grids in the terminal."""
    if not grids:
        return
    delay = 1.0 / fps if fps and fps > 0 else 1.0 / 30.0

    sys.stdout.write(HIDE_CURSOR + CLEAR_SCREEN)
    sys.stdout.flush()
    try:
        while True:
            for grid in grids:
                sys.stdout.write(CURSOR_HOME)
                sys.stdout.write("\n".join(grid_to_lines(grid, pixel)) + "\n")
                sys.stdout.flush()
                time.sleep(delay)
            if not loop:
                break
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


def display_grids_sensehat(grids, delay=0.0, loop=False):
    """Display a sequence of grids on the Sense HAT LED matrix."""
    if not grids:
        return
    from sense_hat import SenseHat

    sense = SenseHat()
    while True:
        for grid in grids:
            display_grid(grid)
            if delay > 0:
                time.sleep(delay)
        if not loop:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image or video to terminal pixel art (truecolor).")
    parser.add_argument("path", help="Path to the input image or video file")
    parser.add_argument("--cols", type=int, default=24, help="Grid width in cells")
    parser.add_argument("--rows", type=int, default=24, help="Grid height in cells")
    parser.add_argument("--video", action="store_true", help="Treat the input as a video file")
    parser.add_argument("--fps", type=float, default=30.0, help="Playback fps for video (default: 30)")
    parser.add_argument("--loop", action="store_true", help="Loop the video playback")
    parser.add_argument("--grid", action="store_true", help="Display the image as a grid in the terminal")
    parser.add_argument("--max-frames", type=int, default=None, help="Stop after this many frames (video only)")
    parser.add_argument("--sensehat", action="store_true", help="Display video grids on the Sense HAT")
    args = parser.parse_args()

    if args.video:
        grids = video_to_grids(args.path, args.cols, args.rows)
        if args.max_frames is not None:
            grids = grids[:args.max_frames]
        if args.sensehat:
            display_grids_sensehat(grids, delay=1.0 / args.fps, loop=args.loop)
        else:
            display_grids_terminal(grids, fps=args.fps, loop=args.loop)
    elif args.grid:
        grid = image_to_grid(args.path, args.cols, args.rows)
        print_pixel_art(grid)
    else:
        grid = image_to_grid(args.path, args.cols, args.rows)
        print_pixel_art(grid)
