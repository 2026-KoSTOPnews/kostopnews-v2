from fastapi import FastAPI

from app.exceptions.custom_exception import CustomException
from app.exceptions.exception_handler import custom_exception_handler, global_exception_handler

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        CustomException,
        custom_exception_handler
    )

    app.add_exception_handler(
        Exception,
        global_exception_handler
    )