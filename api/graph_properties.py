from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .priority_attributes_calculator import PriorityAttributesCalculator

router = APIRouter()

class GraphData(BaseModel):
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
