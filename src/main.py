# from typing import Annotated, List, Optional

import uvicorn
from fastapi import FastAPI
# from fastapi import Depends, FastAPI, Request, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from pydantic import ValidationError

from src.auth.router import router as auth_router


app = FastAPI(title="TrackFolio")

app.include_router(auth_router)


@app.get("/")
def hello():
    return {"message": "Hello from TracFolio!"}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        "src.main:app", reload=True, host="0.0.0.0", port=5000, log_level="info"
    )


# # example of dependency injection
# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}
#
#
# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons
#
#
# @app.get("/users/")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons
#
#
# # setting handler, showing validation error on response to client
# @app.exception_handler(ValidationError)
# async def validation_exeption_handler(request: Request,
#                                       exception: ValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({'detail': exception.errors()})
#     )


if __name__ == "__main__":
    start()
