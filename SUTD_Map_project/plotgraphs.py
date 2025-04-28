import os
import json
import matplotlib
matplotlib.use('TkAgg')  # TkAgg is safest and lightweight
import matplotlib.pyplot as plt

# Folder containing your JSON files
MASTER_FOLDER = 'Master'

# Color mapping based on node type
type_colors = {
    "room": "green",
    "stairs": "blue",
    "lift": "orange",
    "entrance": "red",
    "toilet": "purple",
    "walkway": "cyan",
    "other": "grey"
}

# Function to classify node type
def classify_node(name):
    if "ROOM" in name:
        return "room"
    elif "STAIRS" in name:
        return "stairs"
    elif "LIFT" in name:
        return "lift"
    elif "ENTRANCE" in name:
        return "entrance"
    elif "TOILET" in name:
        return "toilet"
    elif "WALKWAY" in name:
        return "walkway"
    else:
        return "other"

# Function to load and parse one JSON file
def load_graph(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    coordinates = {}
    edges = {}
    types = {}

    for vertex, details in data.items():
        if "Coordinates" not in details:
            raise KeyError(f"Vertex {vertex} missing 'Coordinates'")
        
        x, y = details["Coordinates"]
        coordinates[vertex] = (x, y)
        types[vertex] = classify_node(vertex)

        for neighbor in details.get("Neighbour", {}):
            edges.setdefault(vertex, []).append(neighbor)

    return coordinates, edges, types

# Function to plot one map
def plot_graph(coordinates, edges, types, title):
    plt.figure(figsize=(16, 14))
    plotted_labels = set()

    for vertex, (x, y) in coordinates.items():
        node_type = types.get(vertex, "other")
        if node_type not in plotted_labels:
            plt.scatter(x, y, color=type_colors[node_type], label=node_type)
            plotted_labels.add(node_type)
        else:
            plt.scatter(x, y, color=type_colors[node_type])
        plt.text(x + 0.5, y + 0.5, vertex, fontsize=6)

    for v1, neighbors in edges.items():
        for v2 in neighbors:
            if v2 in coordinates:
                x1, y1 = coordinates[v1]
                x2, y2 = coordinates[v2]
                plt.plot([x1, x2], [y1, y2], 'k-', linewidth=0.5)

    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend(title="Node Types")
    plt.show()

# Main program
def main():
    for filename in sorted(os.listdir(MASTER_FOLDER)):
        if filename.startswith('Building_') and filename.endswith('.json'):
            filepath = os.path.join(MASTER_FOLDER, filename)
            print(f"Processing {filename}...")

            try:
                coordinates, edges, types = load_graph(filepath)
                plot_graph(coordinates, edges, types, title=filename)
            except Exception as e:
                print(f"⚠️ Skipping {filename} due to error: {e}")

if __name__ == "__main__":
    main()

