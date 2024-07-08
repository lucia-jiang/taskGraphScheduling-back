from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .priority_attributes_calculator import PriorityAttributesCalculator
from typing import Optional

router = APIRouter()


class GraphData(BaseModel):
    num_processors: Optional[int] = None
    nodes: list
    edges: list


@router.post("/properties", response_model=dict)
def calculate_properties(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        properties = calculator.obtain_attribute_dict()
        return properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/properties/sl")
async def calculate_sl_steps(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        sl_steps = calculator.calculate_sl_steps()
        return sl_steps
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/properties/lst")
def calculate_properties(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        properties = calculator.calculate_lst_steps()
        return properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/properties/est")
def calculate_properties(graph_data: GraphData):
    try:
        calculator = PriorityAttributesCalculator(graph_data.dict())
        properties = calculator.calculate_est_steps()
        return properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))