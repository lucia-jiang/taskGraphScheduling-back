from graph_from_json import GraphGivenJSON
from get_priority_attributes import PriorityAttributesCalculator

''' REPRESENT GRAPH GIVEN JSON DATA'''
# JSON data representing the graph
json_data = '''{"nodes": [{"id": "1", "weight": 20, "pos": [0, 1]}, {"id": "2", "weight": 20, "pos": [-2, -1]}, {"id": "3", "weight": 20, "pos": [-1, -1]}, {"id": "4", "weight": 15, "pos": [0, -1]}, {"id": "5", "weight": 5, "pos": [1, -1]}, {"id": "6", "weight": 5, "pos": [2, -1]}, {"id": "7", "weight": 10, "pos": [-1.5, -3]}, {"id": "8", "weight": 15, "pos": [0, -3]}, {"id": "9", "weight": 20, "pos": [1.5, -3]}, {"id": "10", "weight": 20, "pos": [0, -4]}], "edges": [{"source": "1", "target": "2", "cost": 8}, {"source": "1", "target": "3", "cost": 4}, {"source": "1", "target": "4", "cost": 2}, {"source": "1", "target": "5", "cost": 8}, {"source": "1", "target": "6", "cost": 4}, {"source": "2", "target": "8", "cost": 4}, {"source": "2", "target": "9", "cost": 8}, {"source": "3", "target": "7", "cost": 8}, {"source": "4", "target": "8", "cost": 8}, {"source": "4", "target": "9", "cost": 2}, {"source": "5", "target": "9", "cost": 8}, {"source": "6", "target": "8", "cost": 8}, {"source": "7", "target": "10", "cost": 2}, {"source": "8", "target": "10", "cost": 4}, {"source": "9", "target": "10", "cost": 8}]}'''

# Create an instance of GraphGivenJSON
graph_from_json = GraphGivenJSON(json_data)

# Parse the JSON data and draw the graph
G = graph_from_json.parse_json() #nx.DiGraph()
graph_from_json.draw_graph()


'''PRIORITY ATTRIBUTES'''
# Create an instance of PriorityAttributesCalculator
priority_calculator = PriorityAttributesCalculator(json_data)

# Obtain all attribute tables
all_attributes = priority_calculator.obtain_attribute_table()
print("All Attributes:")
print(all_attributes)

# Obtain a specific attribute table
t_level_table = priority_calculator.obtain_attribute_table("T-Level")
print("\nT-Level Table:")
print(t_level_table)
