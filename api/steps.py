from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# TODO: change hardcoded step_list
steps_list = [
    {"processor": "1", "node": "3", "time": "5", "total": "5", "desc": "Some description of why this is the step"},
    {"processor": "2", "node": "4", "time": "3", "total": "8", "desc": "Some more description of why this is the step"},
    {"processor": "2", "node": "4", "time": "7", "total": "15", "desc": "Some more description of why this is the step"},
    {"processor": "1", "node": "4", "time": "5", "total": "20", "desc": "Some more description of why this is the step"},
]

@router.get("/steps", response_model=List[Dict[str, str]])
def get_steps():
    return steps_list
