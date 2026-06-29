from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.container import create_daily_pipeline, create_user_pipeline
from app.infrastructure.db.session import engine, Base
from app.services.scheduler.daily_scheduler import DailySentimentScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    app.state.daily_pipeline = create_daily_pipeline()
    app.state.user_pipeline = create_user_pipeline()
    scheduler = DailySentimentScheduler(pipeline=app.state.daily_pipeline)

    start(scheduler)

    yield

    # When service is stopped.
    shutdown(scheduler)

    app.state.user_pipeline.close()
    app.state.daily_pipeline.close()

def start(scheduler):
    print("Service is started.")

    print("Connecting to DataBase...")
    Base.metadata.create_all(bind=engine)

    print("Scheduler is running...")
    scheduler.start()

def shutdown(scheduler):
    scheduler.shutdown()
    print("Scheduler is stopped...")
    print("Service is stopped.")