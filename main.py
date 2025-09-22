import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from note.interface.controller.note_controller import note_router
from user.interface.controller.user_controller import user_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s'
)

app = FastAPI()
app.include_router(user_router)
app.include_router(note_router)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
        request: Request,
        exception: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exception.errors()
    )
