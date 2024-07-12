from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.priority_attributes_calculator import PriorityAttributesCalculator

router = APIRouter()


class GraphData(BaseModel):
    num_processors: int
    nodes: list
    edges: list


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

# @router.post("/dls-steps", response_model=list)
# def dls_steps(graph_data: GraphData):
#     try:
#         calculator = PriorityAttributesCalculator(graph_data.dict())
#         steps = calculator.calculate_dls_steps()
#         return steps
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
# @router.post("/brute-force", response_model=list)
# def brute_force_solution(graph_data: GraphData):
#     try:
#         calculator = PriorityAttributesCalculator(graph_data.dict())
#         steps = calculator.brute_force_solution()
#         return steps
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
