def expand_cluster(cluster_map):
    """Expands the cluster map to add spaces around each resource while preserving shape."""
    # Clone the input map to avoid modifying it in-place
    new_map = [[" " for _ in row] for row in cluster_map]
    width = len(cluster_map[0])
    height = len(cluster_map)

    # Directions for the 8 neighboring cells
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for y in range(height):
        for x in range(width):
            if cluster_map[y][x] == "x":  # Found a resource cell
                # Place the resource in the new map
                new_map[y][x] = "x"

                # Mark surrounding cells as empty (if they’re not already resources)
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and cluster_map[ny][nx] != "x":
                        new_map[ny][nx] = " "

    return new_map

# Example usage
cluster_map = [
    [" ", " ", "x", "x", " "],
    [" ", "x", "x", "x", " "],
    [" ", " ", "x", "x", " "],
]

expanded_map = expand_cluster(cluster_map)

# Print the result
for row in expanded_map:
    print("".join(row))
