import networkx as nx
import matplotlib.pyplot as plt
import json

# Create a directed graph
G = nx.DiGraph()

# Add nodes with weights
G.add_node('1', weight=20)
G.add_node('2', weight=20)
G.add_node('3', weight=20)
G.add_node('4', weight=15)
G.add_node('5', weight=5)
G.add_node('6', weight=5)
G.add_node('7', weight=10)
G.add_node('8', weight=15)
G.add_node('9', weight=20)
G.add_node('10', weight=20)

# Add edges with costs
G.add_edge('1', '2', cost=8)
G.add_edge('1', '3', cost=4)
G.add_edge('1', '4', cost=2)
G.add_edge('1', '5', cost=8)
G.add_edge('1', '6', cost=4)
G.add_edge('2', '8', cost=4)
G.add_edge('2', '9', cost=8)
G.add_edge('3', '7', cost=8)
G.add_edge('4', '8', cost=8)
G.add_edge('4', '9', cost=2)
G.add_edge('5', '9', cost=8)
G.add_edge('6', '8', cost=8)
G.add_edge('7', '10', cost=2)
G.add_edge('8', '10', cost=4)
G.add_edge('9', '10', cost=8)

# Manually specify the positions of nodes
node_positions = {'1': (0, 1), '2': (-2, -1), '3': (-1, -1), '4': (0, -1), '5': (1, -1), '6': (2, -1),
                   '7': (-1.5, -3), '8': (0, -3), '9': (1.5, -3), '10': (0, -4)}

# Draw the graph with fixed positions
nx.draw(G, node_positions, with_labels=False, node_size=1000, node_color='lightblue')  # Draw the nodes without labels
labels = nx.get_edge_attributes(G, 'cost')
nx.draw_networkx_edge_labels(G, node_positions, edge_labels=labels)  # Draw the edge labels

# Draw node labels with name and weight
for node, (x, y) in node_positions.items():
    node_name = node
    node_weight = G.nodes[node]['weight']
    plt.text(x, y, node_name, horizontalalignment='center', verticalalignment='center')
    plt.text(x, y - 0.2, f"w: {node_weight}", horizontalalignment='center', verticalalignment='center')

plt.show()

# Convert graph to JSON format including node positions
graph_data = {
    "nodes": [{"id": node, "weight": G.nodes[node]['weight'], "pos": node_positions[node]} for node in G.nodes()],
    "edges": [{"source": u, "target": v, "cost": G.edges[u, v]['cost']} for u, v in G.edges()]
}

# Serialize the JSON data to a string
json_data = json.dumps(graph_data)

print(json_data)