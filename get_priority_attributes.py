import networkx as nx
from graph_from_json import GraphGivenJSON

# Function to calculate SL (Static Level) for each node
def calculate_sl(G):
    sl = {}
    for node in reversed(list(nx.topological_sort(G))):
        # print('node: ', node)
        # print('weight: ',  G.nodes[node]['weight'])
        # print('succesors: ', list(G.successors(node)))
        # print('predecessors: ', list(G.predecessors(node)))
        successors = list(G.successors(node))
        if len(successors) == 0:
            sl[node] = G.nodes[node]['weight']
        else:
            sl[node] = max(sl[pre] for pre in successors) + G.nodes[node]['weight']
    return sl


# Function to calculate t-level (topological level) for each node
def calculate_t_level(G):
    t_level = {}
    for node in nx.topological_sort(G):
        predecessors = list(G.predecessors(node))
        if len(predecessors) == 0:
            t_level[node] = 0
        else:
            t_level[node] = max(t_level[pred] + G.nodes[pred]['weight'] + G.edges[pred, node]['cost'] for pred in predecessors)
    return t_level

# Function to calculate EST (Earliest Start Time) for each node
def calculate_est(G):
    est = {}
    t_level = calculate_t_level(G)
    for node in G.nodes():
        est[node] = t_level[node]  # EST is equal to t-level for each node
    return est

# Function to calculate LST (Latest Start Time) for each node
def calculate_lst(G):
    lst = {}
    t_level = calculate_t_level(G)
    for node in reversed(list(nx.topological_sort(G))):
        successors = list(G.successors(node))
        if len(successors) == 0: #exist task
            lst[node] = t_level[node]
        else:
            lst[node] = min(lst[succ]-G.edges[node, succ]['cost'] for succ in successors) - G.nodes[node]['weight']
    return lst

# Function to calculate b-level for each node
def calculate_b_level(G,):
    b_level = {}
    for node in reversed(list(nx.topological_sort(G))):
        successors = list(G.successors(node))
        if len(successors) == 0: #exit task
            b_level[node] = G.nodes[node]['weight']
        else:
            b_level[node] = G.nodes[node]['weight'] + max(b_level[succ] + G.edges[node, succ]['cost'] for succ in successors)
    return b_level

# JSON data representing the graph
json_data = '''{"nodes": [{"id": "1", "weight": 20, "pos": [0, 1]}, {"id": "2", "weight": 20, "pos": [-2, -1]}, {"id": "3", "weight": 20, "pos": [-1, -1]}, {"id": "4", "weight": 15, "pos": [0, -1]}, {"id": "5", "weight": 5, "pos": [1, -1]}, {"id": "6", "weight": 5, "pos": [2, -1]}, {"id": "7", "weight": 10, "pos": [-1.5, -3]}, {"id": "8", "weight": 15, "pos": [0, -3]}, {"id": "9", "weight": 20, "pos": [1.5, -3]}, {"id": "10", "weight": 20, "pos": [0, -4]}], "edges": [{"source": "1", "target": "2", "cost": 8}, {"source": "1", "target": "3", "cost": 4}, {"source": "1", "target": "4", "cost": 2}, {"source": "1", "target": "5", "cost": 8}, {"source": "1", "target": "6", "cost": 4}, {"source": "2", "target": "8", "cost": 4}, {"source": "2", "target": "9", "cost": 8}, {"source": "3", "target": "7", "cost": 8}, {"source": "4", "target": "8", "cost": 8}, {"source": "4", "target": "9", "cost": 2}, {"source": "5", "target": "9", "cost": 8}, {"source": "6", "target": "8", "cost": 8}, {"source": "7", "target": "10", "cost": 2}, {"source": "8", "target": "10", "cost": 4}, {"source": "9", "target": "10", "cost": 8}]}'''
graph_from_json = GraphGivenJSON(json_data)
G = graph_from_json.parse_json()
print(G)

# Calculate SL
sl = calculate_sl(G)
print("SL (Static Level):", sl)

# Calculate t-level
t_level = calculate_t_level(G)
print("T-Level:", t_level)

# Calculate EST
est = calculate_est(G)
print("EST (Earliest Start Time):", est)

# Calculate LST
lst = calculate_lst(G)
print("LST (Latest Start Time):", lst)

# Calculate b-level
b_level = calculate_b_level(G)
print("B-Level:", b_level)
