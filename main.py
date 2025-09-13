from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from user.interface.controller.user_controller import user_router

app = FastAPI()
app.include_router(user_router)

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
        request: Request,
        exception: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exception.errors()
    )