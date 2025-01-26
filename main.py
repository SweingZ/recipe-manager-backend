from fastapi import FastAPI
from app.routes.recipes import router as recipe_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(recipe_router, prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Recipe Manager API"}