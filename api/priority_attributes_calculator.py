# api/priority_attributes_calculator.py
import networkx as nx
import pandas as pd
from .graph_from_json import GraphGivenJSON

class PriorityAttributesCalculator:
    def __init__(self, json_data):
        self.graph_from_json = GraphGivenJSON(json_data)
        self.G = self.graph_from_json.parse_json()

    def calculate_sl(self):
        sl = {}
        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) == 0:
                sl[node] = self.G.nodes[node]['weight']
            else:
                sl[node] = max(sl[pre] for pre in successors) + self.G.nodes[node]['weight']
        return sl

    def calculate_t_level(self):
        t_level = {}
        for node in nx.topological_sort(self.G):
            predecessors = list(self.G.predecessors(node))
            if len(predecessors) == 0:
                t_level[node] = 0
            else:
                t_level[node] = max(t_level[pred] + self.G.nodes[pred]['weight'] + self.G.edges[pred, node]['cost'] for pred in predecessors)
        return t_level

    def calculate_est(self):
        est = {}
        t_level = self.calculate_t_level()
        for node in self.G.nodes():
            est[node] = t_level[node]  # EST is equal to t-level for each node
        return est

    def calculate_lst(self):
        lst = {}
        t_level = self.calculate_t_level()
        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) == 0: #exist task
                lst[node] = t_level[node]
            else:
                lst[node] = min(lst[succ]-self.G.edges[node, succ]['cost'] for succ in successors) - self.G.nodes[node]['weight']
        return lst

    def calculate_b_level(self):
        b_level = {}
        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) == 0: #exit task
                b_level[node] = self.G.nodes[node]['weight']
            else:
                b_level[node] = self.G.nodes[node]['weight'] + max(b_level[succ] + self.G.edges[node, succ]['cost'] for succ in successors)
        return b_level

    def obtain_attribute_dict(self, attribute=None):
        if attribute is None:
            return {
                "SL": self.calculate_sl(),
                "T-Level": self.calculate_t_level(),
                "EST": self.calculate_est(),
                "LST": self.calculate_lst(),
                "B-Level": self.calculate_b_level()
            }
        elif attribute == "SL":
            return self.calculate_sl()
        elif attribute == "T-Level":
            return self.calculate_t_level()
        elif attribute == "EST":
            return self.calculate_est()
        elif attribute == "LST":
            return self.calculate_lst()
        elif attribute == "B-Level":
            return self.calculate_b_level()
        else:
            raise ValueError("Invalid attribute name. Please provide one of: 'SL', 'T-Level', 'EST', 'LST', 'B-Level'.")

    def obtain_attribute_table(self, attribute=None):
        if attribute is None:
            all_attributes = {
                "SL": pd.Series(self.calculate_sl()),
                "T-Level": pd.Series(self.calculate_t_level()),
                "EST": pd.Series(self.calculate_est()),
                "B-Level": pd.Series(self.calculate_b_level()),
                "LST": pd.Series(self.calculate_lst())
            }
            df = pd.DataFrame(all_attributes)
            return df
        elif attribute == "SL":
            return pd.DataFrame({"SL": self.calculate_sl()})
        elif attribute == "T-Level":
            return pd.DataFrame({"T-Level": self.calculate_t_level()})
        elif attribute == "EST":
            return pd.DataFrame({"EST": self.calculate_est()})
        elif attribute == "LST":
            return pd.DataFrame({"LST": self.calculate_lst()})
        elif attribute == "B-Level":
            return pd.DataFrame({"B-Level": self.calculate_b_level()})
        else:
            raise ValueError("Invalid attribute name. Please provide one of: 'SL', 'T-Level', 'EST', 'LST', 'B-Level'.")
