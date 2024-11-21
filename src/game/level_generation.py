import random
import json


def get_valid_neighbors(x, y, rows, cols):
    """
    returns a list of valid neighboring cells within the grid bounds
    """
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < rows - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < cols - 1:
        neighbors.append((x, y + 1))
    return neighbors


def collapse(x, y, level, entropy):
    """
    collapses the entropy of a cell to a single tile, selecting
    randomly from the remaining valid options and updating the grid
    """
    if level[x][y] is not None:
        return
    possible_tiles = list(entropy[x][y])
    if not possible_tiles:
        raise ValueError("WFC failed: No valid tiles for position.")
    chosen_tile = random.choice(possible_tiles)
    level[x][y] = chosen_tile
    entropy[x][y] = {chosen_tile}
    return chosen_tile


def propagate(x, y, level, entropy, adjacency_rules, rows, cols):
    """
    propagates constraints from a collapsed cell to its neighbors, updating
    their entropy to ensure tile adjacency rules are respected
    """
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        current_tile = level[cx][cy]
        if current_tile is None:
            continue
        print(f"Propagating constraints from ({cx}, {cy}) with tile '{current_tile}'")
        for nx, ny in get_valid_neighbors(cx, cy, rows, cols):
            if level[nx][ny] is not None:
                continue
            possible_tiles = entropy[nx][ny]
            valid_tiles = {
                tile for tile in possible_tiles if current_tile in adjacency_rules[tile]
            }
            if valid_tiles != possible_tiles:
                print(f"Updating entropy at ({nx}, {ny}): {valid_tiles}")
                entropy[nx][ny] = valid_tiles
                stack.append((nx, ny))


def naive_wave_function_collapse(
    tile_set, adjacency_rules, grid_size, output_filepath=None
):
    """
    implements a naive wave function collapse algorithm to generate a 2d grid-based level
    """
    rows, cols = grid_size
    level = [[None for _ in range(cols)] for _ in range(rows)]
    entropy = [[set(tile_set.keys()) for _ in range(cols)] for _ in range(rows)]
    for _ in range(rows * cols):
        min_entropy = float("inf")
        min_pos = None
        for x in range(rows):
            for y in range(cols):
                if level[x][y] is None and len(entropy[x][y]) < min_entropy:
                    min_entropy = len(entropy[x][y])
                    min_pos = (x, y)
        if min_pos is None:
            break
        cx, cy = min_pos
        collapse(cx, cy, level, entropy)
        propagate(cx, cy, level, entropy, adjacency_rules, rows, cols)
    if output_filepath:
        with open(output_filepath, "w") as file:
            json.dump({"level": level}, file, indent=4)
    return level


# ----- SAMPLE EXECUTION CODE -----

if __name__ == "__main__":

    print("test running level_generation.py...")

    tile_set = {
        "grass": {"color": "green"},
        "water": {"color": "blue"},
        "sand": {"color": "yellow"},
    }

    adjacency_rules = {
        "grass": {"grass", "sand"},
        "water": {"water", "sand"},
        "sand": {"grass", "water", "sand"},
    }

    grid_size = (5, 5)

    generated_level = naive_wave_function_collapse(
        tile_set=tile_set,
        adjacency_rules=adjacency_rules,
        grid_size=grid_size,
        output_filepath="generated_level.json",
    )

    print("Generated Level:")
    for row in generated_level:
        print(row)
