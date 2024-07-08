from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.graph_properties import router as graph_properties_router
from api.algorithms import router as algorithm_steps_router

app = FastAPI()

# CORS settings to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(graph_properties_router, prefix="/graph")
app.include_router(algorithm_steps_router, prefix="/algorithm")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
