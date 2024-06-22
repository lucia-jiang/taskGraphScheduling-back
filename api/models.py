# api/models.py
from pydantic import BaseModel
from typing import List, Dict, Any

class ProcessorTime(BaseModel):
    processor: int
    start_time: int
    end_time: int

class StepDetails(BaseModel):
    processor: int
    node: str
    start_time: int
    end_time: int
    total_time: int
    candidates: List[ProcessorTime]  # Add this to store potential times on each processor

class Step(BaseModel):
    step: str
    details: Any  # Use Any to allow both dict and list types
    desc: str

class HLFETResponse(BaseModel):
    steps: List[Step]

class GraphData(BaseModel):
    nodes: List
    edges: List

class HLFETRequest(BaseModel):
    graph_data: GraphData
    num_processors: int
