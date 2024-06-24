# api/priority_attributes_calculator.py
import networkx as nx
import pandas as pd
from .graph_from_json import GraphGivenJSON

class PriorityAttributesCalculator:
    def __init__(self, json_data, num_processors=3):
        self.graph_from_json = GraphGivenJSON(json_data)
        self.G = self.graph_from_json.parse_json()
        self.num_processors = num_processors

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

    def create_lst_lists(self, lst):
        # Create lists of LST for each task and its dependents
        lst_lists = {}
        for node in self.G.nodes():
            lst_list = [lst[node]]
            for successor in self.G.successors(node):
                lst_list.append(lst[successor])
            lst_lists[node] = lst_list
        return lst_lists

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

    def calculate_hlfet_steps(self):
        steps = []

        # Step 1: Calculate Static Level (SL) for each task
        sl = self.calculate_sl()
        steps.append({
            "step": "Calculate Static Level (SL) for each task.",
            "details": sl,
            "desc": "SL calculated for each node based on its successors."
        })

        # Step 2: List all tasks and sort them by SL in descending order
        sorted_tasks = sorted(sl, key=sl.get, reverse=True)
        steps.append({
            "step": "List all tasks and sort them by SL in descending order.",
            "details": sorted_tasks,
            "desc": "Tasks sorted by SL in descending order."
        })

        # Step 3: Schedule tasks
        scheduled_tasks = []
        processors = {i: 0 for i in
                      range(1, self.num_processors + 1)}  # Initialize all processors with available time 0

        for task in sorted_tasks:
            best_processor = None
            earliest_end_time = float('inf')
            candidates = []

            for processor, available_time in processors.items():
                start_time = available_time
                print("Processing task", task, "initial start_time", start_time)

                # Consider the communication cost
                for predecessor in self.G.predecessors(task):
                    predecessor_task = next((t for t in scheduled_tasks if t['node'] == predecessor), None)
                    print("predecessor_task", predecessor_task)
                    if predecessor_task:
                        if predecessor_task['processor'] == processor:
                            # If the predecessor is on the same processor, no communication cost
                            start_time = max(start_time, predecessor_task['end_time'])
                        else:
                            # If the predecessor is on a different processor, add communication cost
                            start_time = max(start_time,
                                             predecessor_task['end_time'] + self.G.edges[predecessor, task]['cost'])
                    print("Updated start_time after considering predecessor", predecessor, ":", start_time)

                end_time = start_time + self.G.nodes[task]['weight']
                candidates.append({"processor": processor, "start_time": start_time, "end_time": end_time})

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_processor = processor

            processors[best_processor] = earliest_end_time
            scheduled_tasks.append({
                "processor": best_processor,
                "node": task,
                "start_time": start_time,
                "end_time": earliest_end_time,
                "total_time": earliest_end_time,
                "candidates": candidates
            })

            steps.append({
                "step": f"Schedule task {task} with SL {sl[task]}.",
                "details": {
                    "processor": best_processor,
                    "node": task,
                    "start_time": start_time,
                    "end_time": earliest_end_time,
                    "total_time": earliest_end_time,
                    "candidates": candidates
                },
                "desc": f"Scheduled node {task} on processor {best_processor} from time {start_time} to {earliest_end_time}."
            })

        return steps

    def calculate_mcp_steps(self):
        steps = []

        # Step 1: Calculate Latest Start Time (LST) for each task
        lst = self.calculate_lst()
        steps.append({
            "step": "Calculate Latest Start Time (LST) for each task in the graph.",
            "details": lst,
            "desc": "LST calculated for each node."
        })

        # Step 2: For each task, create a list containing its LST and the LST of all its dependent tasks
        lst_lists = self.create_lst_lists(lst)
        steps.append({
            "step": "For each task, create a list containing its LST and the LST of all its dependent tasks.",
            "details": lst_lists,
            "desc": "Lists created for each task containing its LST and the LST of its dependents."
        })

        # Step 3: Sort these lists in ascending order of tasks' LST
        sorted_lst_lists = {task: sorted(lst_list) for task, lst_list in lst_lists.items()}
        steps.append({
            "step": "Sort these lists in ascending order of tasks' LST.",
            "details": sorted_lst_lists,
            "desc": "Lists sorted by tasks' LST in ascending order."
        })

        # Step 4: Create a task list (L) sorted by ascending LST
        sorted_tasks_by_lst = sorted(lst, key=lst.get)
        steps.append({
            "step": "Create a task list (L) sorted by ascending LST. Resolve ties using the sorted lists from Step 2.",
            "details": sorted_tasks_by_lst,
            "desc": "Tasks sorted by ascending LST, with ties resolved using the sorted lists from Step 2."
        })

        # Step 5: Schedule tasks
        scheduled_tasks = []
        processors = {i: 0 for i in
                      range(1, self.num_processors + 1)}  # Initialize all processors with available time 0

        for task in sorted_tasks_by_lst:
            best_processor = None
            earliest_start_time = float('inf')
            candidates = []

            for processor, available_time in processors.items():
                start_time = max(available_time, self.calculate_t_level().get(task, 0))
                end_time = start_time + self.G.nodes[task]['weight']
                candidates.append({"processor": processor, "start_time": start_time, "end_time": end_time})

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_processor = processor

            processors[best_processor] = earliest_start_time + self.G.nodes[task]['weight']
            scheduled_tasks.append({
                "processor": best_processor,
                "node": task,
                "start_time": earliest_start_time,
                "end_time": earliest_start_time + self.G.nodes[task]['weight'],
                "total_time": earliest_start_time + self.G.nodes[task]['weight'],
                "candidates": candidates
            })

            steps.append({
                "step": f"Schedule task {task} with LST {lst[task]}.",
                "details": {
                    "processor": best_processor,
                    "node": task,
                    "start_time": earliest_start_time,
                    "end_time": earliest_start_time + self.G.nodes[task]['weight'],
                    "total_time": earliest_start_time + self.G.nodes[task]['weight'],
                    "candidates": candidates
                },
                "desc": f"Scheduled node {task} on processor {best_processor} from time {earliest_start_time} to {earliest_start_time + self.G.nodes[task]['weight']}."
            })

        return steps