from fastapi import FastAPI
from pydantic import BaseModel

from typing import Optional

app = FastAPI()

#HTTP Request (get)
@app.get("/")
async def root():
    return {"message": "Hello World"}


#Get with parameters
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


#Declare JSON Data Models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/create-items/")
async def create_item(item: Item):
    return item