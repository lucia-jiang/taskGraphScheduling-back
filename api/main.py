from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.steps import router as steps_router
from api.graph_properties import router as graph_properties_router
from api.algorithms import router as hlfet_router

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
app.include_router(steps_router)
app.include_router(graph_properties_router, prefix="/graph")
app.include_router(hlfet_router, prefix="/algorithm")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
