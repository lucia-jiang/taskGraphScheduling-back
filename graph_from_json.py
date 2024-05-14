import networkx as nx
import json
import matplotlib.pyplot as plt

class GraphGivenJSON:
    def __init__(self, json_data):
        self.json_data = json_data
        self.graph_data = json.loads(json_data)
        self.G = nx.DiGraph()

    def parse_json(self):
        # Add nodes with attributes
        for node_data in self.graph_data['nodes']:
            node_id = node_data['id']
            node_weight = node_data['weight']
            node_pos = tuple(node_data['pos'])
            self.G.add_node(node_id, weight=node_weight, pos=node_pos)

        # Add edges with attributes
        for edge_data in self.graph_data['edges']:
            source = edge_data['source']
            target = edge_data['target']
            cost = edge_data['cost']
            self.G.add_edge(source, target, cost=cost)
        return self.G

    def draw_graph(self):
        # Draw the graph
        node_positions = {node: attributes['pos'] for node, attributes in self.G.nodes(data=True)}
        nx.draw(self.G, pos=node_positions, with_labels=False, node_size=1000, node_color='lightblue')
        labels = nx.get_edge_attributes(self.G, 'cost')
        nx.draw_networkx_edge_labels(self.G, pos=node_positions, edge_labels=labels)

        # Add node labels with name and weight
        for node, attributes in self.G.nodes(data=True):
            node_name = node
            node_weight = attributes['weight']
            x, y = node_positions[node]
            plt.text(x, y, node_name, horizontalalignment='center', verticalalignment='center')
            plt.text(x, y - 0.2, f"w: {node_weight}", horizontalalignment='center', verticalalignment='center')

        plt.show()