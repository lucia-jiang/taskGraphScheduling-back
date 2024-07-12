# api/graph_from_json.py
import networkx as nx


class GraphGivenJSON:
    def __init__(self, json_data):
        self.json_data = json_data

    def parse_json(self):
        G = nx.DiGraph()
        for node in self.json_data['nodes']:
            G.add_node(node['id'], weight=node['weight'])
        for edge in self.json_data['edges']:
            G.add_edge(edge['source'], edge['target'], cost=edge['cost'])
        return G
