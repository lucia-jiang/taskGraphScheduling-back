from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.priority_attributes_calculator import PriorityAttributesCalculator

router = APIRouter()

class GraphData(BaseModel):
    nodes: list
    edges: list


# TODO: change hardcoded step_list
steps_list = [
    {"processor": "1", "node": "3", "time": "5", "total": "5", "desc": "Some description of why this is the step"},
    {"processor": "2", "node": "4", "time": "3", "total": "8", "desc": "Some more description of why this is the step"},
    {"processor": "2", "node": "4", "time": "7", "total": "15", "desc": "Some more description of why this is the step"},
    {"processor": "1", "node": "4", "time": "5", "total": "20", "desc": "Some more description of why this is the step"},
]

@router.post("/hlfet-steps", response_model=list)
def hlfet_steps(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        steps = calculator.calculate_hlfet_steps()
        return steps
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mcp-steps", response_model=list)
def mcp_steps(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        steps = calculator.calculate_mcp_steps()
        return steps
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/etf-steps", response_model=list)
def etf_steps(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        steps = calculator.calculate_etf_steps()
        return steps
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
