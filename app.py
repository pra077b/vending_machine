import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.routes import setup_router
from core.settings import api_settings

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

setup_router(app)


if __name__ == "__main__":
    uvicorn.run(
        app,
        port=api_settings.API_PORT,
        log_level=api_settings.LOG_LEVEL,
        log_config=api_settings.log_config
    )

