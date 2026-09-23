from colorama import just_fix_windows_console
from termcolor import colored
trans_flag= ['cyan','magenta', 'white', 'magenta','cyan']
rainbow = ['red','yellow','green','blue','magenta']
flags = [trans_flag,rainbow]
"""
Convert an image (or video) into terminal pixel art using true 24-bit color.

How it works:
  1. cv2.resize(img, (cols, rows), interpolation=cv2.INTER_AREA) shrinks the
     image down to one pixel per grid cell. INTER_AREA is a box filter, so
     each output pixel is literally the AVERAGE of the pixels in that region
     of the original image -- that's the "average each grid cell" step,
     done for free with no manual looping.
  2. Each averaged pixel is printed directly as a truecolor ANSI background
     color -- no palette or nearest-color matching needed, since modern
     terminals (iTerm2, Windows Terminal, most Linux terminals, VS Code's
     integrated terminal, etc.) support the full 16.7 million RGB colors.
  3. For video, the same per-frame downscale+print is repeated for every
     frame read from cv2.VideoCapture, with the cursor moved back to the
     top of the frame (instead of clearing the screen) to keep playback
     smooth and flicker-free.

Usage:
    python3 image_to_pixelart.py path/to/image.png --cols 32 --rows 32
    python3 image_to_pixelart.py path/to/clip.mp4 --cols 32 --rows 18 --video
    python3 image_to_pixelart.py path/to/clip.mp4 --cols 32 --rows 18 --video --fps 15 --loop


    from sense_hat import SenseHat
import time

sense = SenseHat()

while True:
        sense.set_pixel(0, 2, (0, 0, 255))
        time.sleep(1)
        sense.set_pixel(7, 4, (255, 0, 0))
        time.sleep(1)
"""

import argparse
import sys
import time
import cv2
import numpy as np
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
    for line in grid_to_lines(grid, pixel):
        print(line)


def save_preview(grid, out_path, cell_size=20):
    """Render the grid to a PNG so you can preview it without a terminal."""
    rows, cols = len(grid), len(grid[0])
    canvas = np.zeros((rows * cell_size, cols * cell_size, 3), dtype=np.uint8)
    for r, row in enumerate(grid):
        for c, rgb in enumerate(row):
            bgr = (rgb[2], rgb[1], rgb[0])
            y0, y1 = r * cell_size, (r + 1) * cell_size
            x0, x1 = c * cell_size, (c + 1) * cell_size
            canvas[y0:y1, x0:x1] = bgr
    cv2.imwrite(out_path, canvas)


def display_grid(grid):
    """Display the grid on the Sense HAT LED matrix."""
    from sense_hat import SenseHat
    sense = SenseHat()
    for r, row in enumerate(grid):
        for c, rgb in enumerate(row):
            sense.set_pixel(c, r, rgb)




def video_to_terminal(path, cols, rows, fps=None, pixel="  ", loop=False, max_frames=None):
    """
    Play a video file (mp4, mov, avi, etc.) as terminal pixel art.

    Each frame is downscaled to a cols x rows grid exactly like a still
    image, then printed. Between frames the cursor is moved back to the
    top-left (rather than clearing the screen) so playback doesn't flicker.

    Args:
        path:       path to the video file
        cols, rows: grid size in terminal cells
        fps:        target playback fps. Defaults to the video's own fps
                    (from cv2.CAP_PROP_FPS, falling back to 30 if unknown).
        pixel:      string used per cell (default two spaces, like image mode)
        loop:       if True, replay from the start when the video ends
        max_frames: optional cap on how many frames to play (useful for
                    testing without watching the whole clip)
    """
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {path}")

    src_fps = cap.get(cv2.CAP_PROP_FPS)
    if not src_fps or src_fps <= 0:
        src_fps = 30.0
    target_fps = fps if fps and fps > 0 else src_fps
    delay = 1.0 / target_fps

    sys.stdout.write(HIDE_CURSOR + CLEAR_SCREEN)
    sys.stdout.flush()

    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                if loop:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                break

            grid = frame_to_grid(frame, cols, rows)
            lines = grid_to_lines(grid, pixel)

            sys.stdout.write(CURSOR_HOME)
            sys.stdout.write("\n".join(lines) + "\n")
            sys.stdout.flush()

            frame_count += 1
            if max_frames is not None and frame_count >= max_frames:
                break

            time.sleep(delay)
    finally:
        cap.release()
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image or video to terminal pixel art (truecolor).")
    parser.add_argument("path", help="Path to the input image or video file")
    parser.add_argument("--cols", type=int, default=24, help="Grid width in cells")
    parser.add_argument("--rows", type=int, default=24, help="Grid height in cells")
    parser.add_argument("--preview", default=None, help="Optional path to save a PNG preview (image mode only)")
    parser.add_argument("--video", action="store_true", help="Treat the input as a video file")
    parser.add_argument("--fps", type=float, default=None, help="Playback fps for video (defaults to the source video's fps)")
    parser.add_argument("--loop", action="store_true", help="Loop the video playback")
    parser.add_argument("--max-frames", type=int, default=None, help="Stop after this many frames (video only)")
    args = parser.parse_args()

    if args.video:
        video_to_terminal(
            args.path,
            args.cols,
            args.rows,
            fps=args.fps,
            loop=args.loop,
            max_frames=args.max_frames,
        )
    else:
        grid = image_to_grid(args.path, args.cols, args.rows)
        print_pixel_art(grid)

        if args.preview:
            save_preview(grid, args.preview)
            print(f"\nSaved preview to {args.preview}")
