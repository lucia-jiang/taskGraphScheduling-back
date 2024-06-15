from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()

# CORS settings to allow all origins (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

steps_list = [
    {"processor": "1", "node": "3", "time": "5", "total": "5"},
    {"processor": "2", "node": "4", "time": "3", "total": "8"},
]

@app.get("/steps", response_model=List[Dict[str, str]])
def get_steps():
    return steps_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
