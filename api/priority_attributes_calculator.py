# api/priority_attributes_calculator.py
import itertools

import networkx as nx
import pandas as pd
from .graph_from_json import GraphGivenJSON

class PriorityAttributesCalculator:
    def __init__(self, json_data):
        self.graph_from_json = GraphGivenJSON(json_data)
        self.G = self.graph_from_json.parse_json()
        self.num_processors = json_data['num_processors']

    def calculate_sl(self):
        sl = {}
        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) == 0:
                sl[node] = self.G.nodes[node]['weight']
            else:
                sl[node] = max(sl[pre] for pre in successors) + self.G.nodes[node]['weight']
        return sl

    def calculate_sl_steps(self):
        steps = []
        sl = {}

        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) == 0:
                sl[node] = self.G.nodes[node]['weight']
                steps.append({
                    "step": f"Calculate SL for node {node}",
                    "details": {"successors": successors, "sl": sl[node]},
                    "desc": f"Node {node} has no successors. SL is its weight {self.G.nodes[node]['weight']}."
                })
            else:
                max_successor_sl = max(sl[pre] for pre in successors)
                sl[node] = max_successor_sl + self.G.nodes[node]['weight']
                steps.append({
                    "step": f"Calculate SL for node {node}",
                    "details": {"successors": successors, "max_successor_sl": max_successor_sl, "sl": sl[node]},
                    "desc": f"Node {node} has successors {successors}. SL is its weight {self.G.nodes[node]['weight']} + max successor SL {max_successor_sl}."
                })
        return steps

    def calculate_t_level(self):
        t_level = {}
        for node in nx.topological_sort(self.G):
            predecessors = list(self.G.predecessors(node))
            if len(predecessors) == 0:
                t_level[node] = 0
            else:
                t_level[node] = max(t_level[pred] + self.G.nodes[pred]['weight'] + self.G.edges[pred, node]['cost'] for pred in predecessors)
        return t_level

    def calculate_est_steps(self):
        steps = []
        est = {}

        for node in nx.topological_sort(self.G):
            predecessors = list(self.G.predecessors(node))
            if len(predecessors) == 0:
                est[node] = 0
                steps.append({
                    "step": f"Calculate EST for node {node}",
                    "details": {"predecessors": predecessors, "EST": est[node]},
                    "desc": f"Node {node} has no predecessors. EST is initialized to 0."
                })
            else:
                max_pred_est = max(
                    est[pred] + self.G.nodes[pred]['weight'] + self.G.edges[pred, node]['cost'] for pred in
                    predecessors)
                est[node] = max_pred_est
                steps.append({
                    "step": f"Calculate EST for node {node}",
                    "details": {"predecessors": predecessors, "max_pred_est": max_pred_est,
                                "EST": est[node]},
                    "desc": f"Node {node} has predecessors {predecessors}. EST is the maximum of predecessors' EST + node weight + edge cost."
                })

        return steps

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

    def calculate_lst_steps(self):
        steps = []
        lst = {}

        # Calculate t_level first
        est_steps = self.calculate_est_steps()
        for step in est_steps:
            steps.append(step)

        t_level = self.calculate_t_level()

        # Initialize LST for end nodes
        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) == 0:  # End node
                lst[node] = t_level[node]
                steps.append({
                    "step": f"Calculate LST for node {node}",
                    "details": {"Successors": successors, "LST": lst[node]},
                    "desc": f"Node {node} is an end node. LST is initialised to EST, which is {t_level[node]}."
                })

        # Calculate LST for other nodes
        for node in reversed(list(nx.topological_sort(self.G))):
            successors = list(self.G.successors(node))
            if len(successors) > 0:  # Non-end node
                min_successor_lst = min(lst[succ] - self.G.edges[node, succ]['cost'] for succ in successors)
                lst[node] = min_successor_lst - self.G.nodes[node]['weight']
                steps.append({
                    "step": f"Calculate LST for node {node}",
                    "details": {"successors": successors, "min_successor_lst": min_successor_lst, "LST": lst[node]},
                    "desc": f"Node {node} has successors {successors}. LST is the minimum of (successors' LST - edge cost) - node weight."
                })

        return steps

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
                predecessor_details = []

                # Consider the communication cost
                for predecessor in self.G.predecessors(task):
                    predecessor_task = next((t for t in scheduled_tasks if t['node'] == predecessor), None)
                    if predecessor_task:
                        if predecessor_task['processor'] == processor:
                            # If the predecessor is on the same processor, no communication cost
                            start_time = max(start_time, predecessor_task['end_time'])
                            comm_cost = 0
                        else:
                            # If the predecessor is on a different processor, add communication cost
                            start_time = max(start_time,
                                             predecessor_task['end_time'] + self.G.edges[predecessor, task]['cost'])
                            comm_cost = self.G.edges[predecessor, task]['cost']
                        predecessor_details.append({
                            "predecessor": predecessor,
                            "processor": predecessor_task['processor'],
                            "same_processor": predecessor_task['processor'] == processor,
                            "pred_start_time": predecessor_task['start_time'],
                            "pred_end_time": predecessor_task['end_time'],
                            "comm_cost": comm_cost,
                            "available_time": available_time,
                            "max_start_time": start_time
                        })

                end_time = start_time + self.G.nodes[task]['weight']
                candidates.append({
                    "processor": processor,
                    "start_time": start_time,
                    "end_time": end_time,
                    "node_weight": self.G.nodes[task]['weight'],
                    "predecessor_details": predecessor_details
                })

                if end_time < earliest_end_time:
                    earliest_start_time = start_time
                    earliest_end_time = end_time
                    best_processor = processor

            processors[best_processor] = earliest_end_time
            scheduled_tasks.append({
                "processor": best_processor,
                "node": task,
                "start_time": earliest_start_time,
                "end_time": earliest_end_time,
                "total_time": earliest_end_time,
                "candidates": candidates
            })

            steps.append({
                "step": f"Schedule task {task} with SL {sl[task]}.",
                "details": {
                    "processor": best_processor,
                    "node": task,
                    "start_time": earliest_start_time,
                    "end_time": earliest_end_time,
                    "total_time": earliest_end_time,
                    "candidates": candidates
                },
                "desc": f"Scheduled node {task} on processor {best_processor} from time {earliest_start_time} to {earliest_end_time}."
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

        # Step 2: List all tasks and sort them by LST in ascending order
        sorted_tasks_by_lst = sorted(lst, key=lst.get)
        steps.append({
            "step": "List all tasks and sort them by LST in ascending order.",
            "details": sorted_tasks_by_lst,
            "desc": "Tasks sorted by LST in ascending order."
        })

        # Step 3: Schedule tasks
        scheduled_tasks = []
        processors = {i: 0 for i in
                      range(1, self.num_processors + 1)}  # Initialize all processors with available time 0

        for task in sorted_tasks_by_lst:
            best_processor = None
            earliest_start_time = float('inf')
            candidates = []

            for processor, available_time in processors.items():
                start_time = available_time
                predecessor_details = []

                # Consider the communication cost
                for predecessor in self.G.predecessors(task):
                    predecessor_task = next((t for t in scheduled_tasks if t['node'] == predecessor), None)
                    if predecessor_task:
                        if predecessor_task['processor'] == processor:
                            # If the predecessor is on the same processor, no communication cost
                            start_time = max(start_time, predecessor_task['end_time'])
                            comm_cost = 0
                        else:
                            # If the predecessor is on a different processor, add communication cost
                            comm_cost = self.G.edges[predecessor, task]['cost']
                            start_time = max(start_time, predecessor_task['end_time'] + comm_cost)
                        predecessor_details.append({
                            "predecessor": predecessor,
                            "processor": predecessor_task['processor'],
                            "same_processor": predecessor_task['processor'] == processor,
                            "pred_start_time": predecessor_task['start_time'],
                            "pred_end_time": predecessor_task['end_time'],
                            "comm_cost": comm_cost,
                            "available_time": available_time,
                            "max_start_time": start_time
                        })


                end_time = start_time + self.G.nodes[task]['weight']
                candidates.append({
                    "processor": processor,
                    "start_time": start_time,
                    "end_time": end_time,
                    "node_weight": self.G.nodes[task]['weight'],
                    "predecessor_details": predecessor_details
                })

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

    def calculate_eexct(self):  # earliest execution time
        est = {}
        for node in nx.topological_sort(self.G):
            if not list(self.G.predecessors(node)):
                est[node] = 0
            else:
                est[node] = max(est[pred] + self.G.nodes[pred]['weight'] + self.G.edges[pred, node]['cost']
                                for pred in self.G.predecessors(node))
        return est

    def calculate_etf_steps(self):
        steps = []

        # Step 1: Calculate Static Level (SL) for each task
        sl = self.calculate_sl()
        steps.append({
            "step": "Calculate Static Level (SL) for each task.",
            "details": sl,
            "desc": "SL calculated based on task dependencies and weights."
        })

        # Step 2: Initialise the ready list with the entry node (root node)
        ready_nodes = [node for node in self.G.nodes if not list(self.G.predecessors(node))]
        steps.append({
            "step": "Initialize ready nodes list with entry nodes.",
            "details": ready_nodes,
            "desc": "Entry nodes identified and added to the ready list."
        })

        # Step 3: While there are nodes in the ready list
        scheduled_tasks = []
        processor_available_times = {i: 0 for i in range(1, self.num_processors + 1)}

        while ready_nodes:
            # Calculate earliest execution start time for each node on all processors
            earliest_execution_times = {}

            for node in ready_nodes:
                earliest_execution_times[node] = []
                for processor, available_time in processor_available_times.items():
                    start_time = available_time
                    predecessor_details = []

                    # Consider the communication cost
                    for predecessor in self.G.predecessors(node):
                        predecessor_task = next((t for t in scheduled_tasks if t['node'] == predecessor), None)
                        if predecessor_task:
                            if predecessor_task['processor'] == processor:
                                start_time = max(start_time, predecessor_task['end_time'])
                                comm_cost = 0
                            else:
                                comm_cost = self.G.edges[predecessor, node]['cost']
                                start_time = max(start_time, predecessor_task['end_time'] + comm_cost)

                            predecessor_details.append({
                                "predecessor": predecessor,
                                "processor": predecessor_task['processor'],
                                "same_processor": predecessor_task['processor'] == processor,
                                "pred_start_time": predecessor_task['start_time'],
                                "pred_end_time": predecessor_task['end_time'],
                                "comm_cost": comm_cost,
                                "available_time": available_time,
                                "max_start_time": start_time
                            })

                    end_time = start_time + self.G.nodes[node]['weight']
                    earliest_execution_times[node].append({
                        "processor": processor,
                        "start_time": start_time,
                        "end_time": end_time,
                        "node_weight": self.G.nodes[node]['weight'],
                        "predecessor_details": predecessor_details
                    })

            # Choose the node-processor pair with the earliest execution start time
            best_node = None
            best_processor = None
            earliest_start_time = float('inf')
            highest_sl = -1

            for node, processor_times in earliest_execution_times.items():
                for times in processor_times:
                    start_time = times['start_time']
                    if start_time < earliest_start_time or (
                            start_time == earliest_start_time and sl[node] > highest_sl):
                        best_node = node
                        best_processor = times['processor']
                        earliest_start_time = start_time
                        highest_sl = sl[node]

            # Schedule the best_node on the best_processor
            end_time = earliest_start_time + self.G.nodes[best_node]['weight']
            best_predecessor_details = next((t['predecessor_details'] for t in earliest_execution_times[best_node] if
                                             t['processor'] == best_processor), [])

            # Ensure correct recording of predecessor details
            candidates = []
            for times in earliest_execution_times[best_node]:
                candidates.append({
                    "processor": times['processor'],
                    "start_time": times['start_time'],
                    "end_time": times['end_time'],
                    "node_weight": times['node_weight'],
                    "predecessor_details": times['predecessor_details']
                })

            scheduled_task = {
                "processor": best_processor,
                "node": best_node,
                "start_time": earliest_start_time,
                "end_time": end_time,
                "total_time": end_time,
                "predecessor_details": best_predecessor_details,
                "candidates": candidates
            }
            scheduled_tasks.append(scheduled_task)

            # Update processor_available_times for the chosen processor
            processor_available_times[best_processor] = end_time

            # Remove the scheduled node from ready_nodes
            ready_nodes.remove(best_node)

            # Add newly ready nodes (nodes whose dependencies are satisfied) to ready_nodes
            for succ in self.G.successors(best_node):
                if all(pred in [task['node'] for task in scheduled_tasks] for pred in self.G.predecessors(succ)):
                    ready_nodes.append(succ)

            # Record this step in the steps list
            steps.append({
                "step": f"Schedule task {best_node} with SL {sl[best_node]}.",
                "details": scheduled_task,
                "desc": f"Scheduled node {best_node} on processor {best_processor} from time {earliest_start_time} to {end_time}."
            })

        return steps

    #TODO: not working
    def calculate_dls_steps(self):
        steps = []

        # Step 1: Calculate Static Level (SL) for each task
        sl = self.calculate_sl()
        steps.append({
            "step": "Calculate Static Level (SL) for each task.",
            "details": sl,
            "desc": "SL calculated for each node based on its successors."
        })

        # Step 2: Initialize ready nodes list with entry nodes
        ready_nodes = [node for node in self.G.nodes() if self.G.in_degree(node) == 0]
        steps.append({
            "step": "Initialize ready nodes list with entry nodes.",
            "details": ready_nodes,
            "desc": "Entry nodes identified and added to the ready list."
        })

        scheduled_tasks = []
        processors = {i: 0 for i in
                      range(1, self.num_processors + 1)}  # Initialize all processors with available time 0

        # Step 3: Schedule tasks
        while ready_nodes:
            best_task = None
            best_processor = None
            best_dl = float('-inf')
            best_start_time = None
            candidates = []

            for task in ready_nodes:
                for processor, available_time in processors.items():
                    start_time = available_time

                    # Consider the communication cost
                    for predecessor in self.G.predecessors(task):
                        predecessor_task = next((t for t in scheduled_tasks if t['node'] == predecessor), None)
                        if predecessor_task:
                            if predecessor_task['processor'] == processor:
                                start_time = max(start_time, predecessor_task['end_time'])
                            else:
                                start_time = max(start_time,
                                                 predecessor_task['end_time'] + self.G.edges[predecessor, task]['cost'])

                    dl = sl[task] - start_time
                    end_time = start_time + self.G.nodes[task]['weight']
                    candidates.append(
                        {"processor": processor, "node": task, "start_time": start_time, "end_time": end_time,
                         "dl": dl})

                    if dl > best_dl:
                        best_dl = dl
                        best_task = task
                        best_processor = processor
                        best_start_time = start_time

            # Schedule the best task
            processors[best_processor] = best_start_time + self.G.nodes[best_task]['weight']
            scheduled_tasks.append({
                "processor": best_processor,
                "node": best_task,
                "start_time": best_start_time,
                "end_time": best_start_time + self.G.nodes[best_task]['weight'],
                "total_time": best_start_time + self.G.nodes[best_task]['weight'],
                "candidates": candidates
            })

            steps.append({
                "step": f"Schedule task {best_task} with DL {best_dl}.",
                "details": {
                    "processor": best_processor,
                    "node": best_task,
                    "start_time": best_start_time,
                    "end_time": best_start_time + self.G.nodes[best_task]['weight'],
                    "total_time": best_start_time + self.G.nodes[best_task]['weight'],
                    "candidates": candidates
                },
                "desc": f"Scheduled node {best_task} on processor {best_processor} from time {best_start_time} to {best_start_time + self.G.nodes[best_task]['weight']}."
            })

            # Remove the scheduled task from ready nodes
            ready_nodes.remove(best_task)

            # Add newly ready nodes to the ready list
            for successor in self.G.successors(best_task):
                if all(predecessor in [t['node'] for t in scheduled_tasks] for predecessor in
                       self.G.predecessors(successor)):
                    ready_nodes.append(successor)

        return steps

    #TODO: BRUTE FORCE SOLUTION
    def brute_force_solution(self):
        processors = {i: 0 for i in range(1, self.num_processors + 1)}
        schedule = []
        task_start_times = {}

        tasks = list(self.G.nodes)

        for task in tasks:
            est = 0
            for pred in self.G.predecessors(task):
                pred_end_time = task_start_times[pred] + self.G.nodes[pred]['weight']
                if task_start_times[pred]['processor'] == processor:
                    est = max(est, pred_end_time)
                else:
                    est = max(est, pred_end_time + self.G.edges[pred, task]['cost'])

            best_processor = None
            earliest_start_time = float('inf')
            candidates = []

            for processor, available_time in processors.items():
                start_time = available_time

                # Consider the communication cost
                for predecessor in self.G.predecessors(task):
                    predecessor_task = next((t for t in schedule if t['task'] == predecessor), None)
                    if predecessor_task:
                        if predecessor_task['processor'] == processor:
                            start_time = max(start_time, predecessor_task['end_time'])
                        else:
                            start_time = max(start_time,
                                             predecessor_task['end_time'] + self.G.edges[predecessor, task]['cost'])

                end_time = start_time + self.G.nodes[task]['weight']
                candidates.append({
                    "processor": processor,
                    "start_time": start_time,
                    "end_time": end_time
                })

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_processor = processor

            processors[best_processor] = earliest_start_time + self.G.nodes[task]['weight']
            schedule.append({
                'task': task,
                'processor': best_processor,
                'start_time': earliest_start_time,
                'end_time': earliest_start_time + self.G.nodes[task]['weight'],
                'total_time': earliest_start_time + self.G.nodes[task]['weight'],
                'candidates': candidates
            })

            task_start_times[task] = {
                'processor': best_processor,
                'start_time': earliest_start_time,
                'end_time': earliest_start_time + self.G.nodes[task]['weight'],
                'total_time': earliest_start_time + self.G.nodes[task]['weight'],
                'candidates': candidates
            }

        return schedule