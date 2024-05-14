import networkx as nx
import json
import matplotlib.pyplot as plt

# JSON data representing the graph
json_data = '''{"nodes": [{"id": "1", "weight": 20, "pos": [0, 1]}, {"id": "2", "weight": 20, "pos": [-2, -1]}, {"id": "3", "weight": 20, "pos": [-1, -1]}, {"id": "4", "weight": 15, "pos": [0, -1]}, {"id": "5", "weight": 5, "pos": [1, -1]}, {"id": "6", "weight": 5, "pos": [2, -1]}, {"id": "7", "weight": 10, "pos": [-1.5, -3]}, {"id": "8", "weight": 15, "pos": [0, -3]}, {"id": "9", "weight": 20, "pos": [1.5, -3]}, {"id": "10", "weight": 20, "pos": [0, -4]}], "edges": [{"source": "1", "target": "2", "cost": 8}, {"source": "1", "target": "3", "cost": 4}, {"source": "1", "target": "4", "cost": 2}, {"source": "1", "target": "5", "cost": 8}, {"source": "1", "target": "6", "cost": 4}, {"source": "2", "target": "8", "cost": 4}, {"source": "2", "target": "9", "cost": 8}, {"source": "3", "target": "7", "cost": 8}, {"source": "4", "target": "8", "cost": 8}, {"source": "4", "target": "9", "cost": 2}, {"source": "5", "target": "9", "cost": 8}, {"source": "6", "target": "8", "cost": 8}, {"source": "7", "target": "10", "cost": 2}, {"source": "8", "target": "10", "cost": 4}, {"source": "9", "target": "10", "cost": 8}]}'''

# Parse JSON data
graph_data = json.loads(json_data)

# Create an empty graph
G = nx.DiGraph()

# Add nodes with attributes
for node_data in graph_data['nodes']:
    node_id = node_data['id']
    node_weight = node_data['weight']
    node_pos = tuple(node_data['pos'])
    G.add_node(node_id, weight=node_weight, pos=node_pos)

# Add edges with attributes
for edge_data in graph_data['edges']:
    source = edge_data['source']
    target = edge_data['target']
    cost = edge_data['cost']
    G.add_edge(source, target, cost=cost)

# Draw the graph
node_positions = {node: attributes['pos'] for node, attributes in G.nodes(data=True)}
nx.draw(G, pos=node_positions, with_labels=False, node_size=1000, node_color='lightblue')
labels = nx.get_edge_attributes(G, 'cost')
nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=labels)

# Add node labels with name and weight
for node, attributes in G.nodes(data=True):
    node_name = node
    node_weight = attributes['weight']
    x, y = node_positions[node]
    plt.text(x, y, node_name, horizontalalignment='center', verticalalignment='center')
    plt.text(x, y - 0.2, f"w: {node_weight}", horizontalalignment='center', verticalalignment='center')

plt.show()
