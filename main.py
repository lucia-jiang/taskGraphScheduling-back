from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.graph_properties import router as graph_properties_router
from api.algorithms import router as algorithm_steps_router

app = FastAPI()

# CORS settings to allow specific origins (replace with your frontend URL)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://task-graph-scheduling-lucia-jiang-2e58e4e5.koyeb.app",
    "https://lucia-jiang.github.io"
]

# CORS settings to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(graph_properties_router, prefix="/graph")
app.include_router(algorithm_steps_router, prefix="/algorithm")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
