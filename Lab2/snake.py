def generate_hamiltonian_cycle(cols=8, rows=8):
    """Generate a Hamiltonian cycle for a grid using boustrophedon pattern.
    Returns a list of (x, y) coordinates that form a complete cycle."""
    path = []
    for row in range(rows):
        if row % 2 == 0:
            # Even rows: left to right
            for col in range(cols):
                path.append((col, row))
        else:
            # Odd rows: right to left
            for col in range(cols - 1, -1, -1):
                path.append((col, row))
    return path


def create_snake_grid(path, length=10, head_color=(0, 255, 0), body_color=(0, 100, 0), bg_color=(0, 0, 0)):
    """Create an 8x8 grid with a snake following a path.

    Args:
        path: List of (x, y) coordinates (from generate_hamiltonian_cycle)
        length: Length of the snake
        head_color: RGB tuple for snake head
        body_color: RGB tuple for snake body
        bg_color: RGB tuple for background

    Returns:
        8x8 grid (list of lists with RGB tuples)
    """
    grid = [[bg_color] * 8 for _ in range(8)]

    # Head is at position 0, body extends for 'length' squares
    for i in range(min(length, len(path))):
        x, y = path[i]
        if i == 0:
            grid[y][x] = head_color
        else:
            grid[y][x] = body_color

    return grid


def create_animated_snake(path, length=10, frames=64, head_color=(0, 255, 0),
                         body_color=(0, 100, 0), bg_color=(0, 0, 0)):
    """Create a series of frames showing snake moving around the cycle.

    Args:
        path: List of (x, y) coordinates
        length: Length of the snake
        frames: Number of animation frames
        head_color, body_color, bg_color: RGB tuples

    Returns:
        List of grids for animation
    """
    grids = []
    path_len = len(path)

    for start_idx in range(frames):
        grid = [[bg_color] * 8 for _ in range(8)]

        for i in range(length):
            idx = (start_idx + i) % path_len
            x, y = path[idx]
            if i == 0:
                grid[y][x] = head_color
            else:
                grid[y][x] = body_color

        grids.append(grid)

    return grids


# Generate the standard path
hamiltonian_path = generate_hamiltonian_cycle()

# Example snake grids
snake_length_10 = create_snake_grid(hamiltonian_path, length=10)
snake_length_20 = create_snake_grid(hamiltonian_path, length=20)

# Example animated snake (64 frames = full cycle)
snake_animation = create_animated_snake(hamiltonian_path, length=10, frames=64)

if __name__ == "__main__":
    from image_to_grid import display_grid
    import time

    display_grid(snake_length_10)
    time.sleep(1)
    display_grid(snake_length_20)
    time.sleep(1)
    for frame in snake_animation:
        display_grid(frame)
        time.sleep(0.1)