from fastapi import FastAPI

from app.core.exception import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.router import api_router

app = FastAPI(title="Daily News Sentiment API", lifespan=lifespan)
register_exception_handlers(app)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
