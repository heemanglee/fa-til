from fastapi import FastAPI

from user.interface.controller.user_controller import user_router

app = FastAPI()
app.include_router(user_router)