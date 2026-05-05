from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.points_router import points_router

app = FastAPI(
    title="Thermal Shield API",
    description="Backend for filtering InPost parcel lockers based on extreme weather conditions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(points_router)

@app.get("/")
async def root():
    return {"message": "Thermal Shield API is running. Go to /docs to test it!"}