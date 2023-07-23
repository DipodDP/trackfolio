# from typing import Annotated, List, Optional

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router import router as auth_router
from src.database import async_session_maker
from src.models import Stock

# from fastapi import Depends, FastAPI, Request, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from pydantic import ValidationError


app = FastAPI(title="TrackFolio")

app.include_router(auth_router)

templates = Jinja2Templates("src/templates")


class StockRequest(BaseModel):
    symbol: str


async def get_db():
    async with async_session_maker() as session:
        yield session


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "home/dashboard.html",
        {
            "request": request,
        },
    )


@app.post("/stock")
async def create_stock(request: StockRequest, db: AsyncSession = Depends(get_db)):
    stock = Stock()
    stock.symbol = request.symbol
    db.add(stock)
    await db.commit()

    return {"code": "success", "message": "stock_created"}


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
