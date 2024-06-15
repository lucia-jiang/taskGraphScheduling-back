from get_priority_attributes import PriorityAttributesCalculator

class HLFETScheduler:
    def __init__(self, json_data, num_processors):
        self.priority_calculator = PriorityAttributesCalculator(json_data)
        self.G = self.priority_calculator.G
        self.num_processors = num_processors

    def schedule_tasks(self):
        sl = self.priority_calculator.calculate_sl()
        sorted_nodes = sorted(sl.keys(), key=lambda x: sl[x], reverse=True)
        scheduled_tasks = []

        while sorted_nodes:
            vi = sorted_nodes.pop(0)  # Dequeue vi
            processors_est = {}  # Dictionary to store earliest execution start time for vi in all processors

            # Compute earliest execution start time for vi in all processors
            for processor in range(self.num_processors):
                est_vi = self.calculate_earliest_start_time(vi, processor)
                processors_est[processor] = est_vi

            # Schedule vi to the processor that minimizes the node earliest execution start time
            min_est_processor = min(processors_est, key=processors_est.get)
            scheduled_tasks.append((vi, min_est_processor, processors_est[min_est_processor]))

        return scheduled_tasks

    def calculate_earliest_start_time(self, node, processor):
        predecessors = list(self.G.predecessors(node))
        if not predecessors:
            return 0  # If node has no predecessors, earliest start time is 0
        else:
           #TODO
            return 0
