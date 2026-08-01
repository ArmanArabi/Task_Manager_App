from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging


logger = logging.getLogger("app_exceptions")

def setup_exception_handlers(app):
    
    ## 1. handle the logical error like 404 or 200
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"Logical Error: {exc.detail} | Status: {exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={'error': True, 'status_code': exc.status_code, 'detail': str(exc.detail)}
        )

    ## 2. Server-side Pydantic Errors (Invalid data from server)
    @app.exception_handler(ResponseValidationError)
    async def response_validation_handler(request: Request, exc: ResponseValidationError):
        logger.error(f"Server Error: {exc.detail}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={'error': True, 'status_code': 422, 'detail': str(exc.errors()), 'content': 'Server response error'}
        )

    ## 3. Client-side Pydantic Errors (Invalid input data from client)
    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Client Error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={'error': True, 'status_code': 422, 'detail': str(exc.errors()), 'content': 'Invalid client data'}
        )

    ## 4. Database Errors (this error occure in database layer, pydantic dont know what happend)
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database Error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'error': True, 'status_code': 500, 'detail': "Database error occurred", 'content': 'database error'}
        )

    ## 5. The Final Safety Net (Global Exception)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Unhandled Error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'error': True, 'detail': 'Internal server error', 'content': 'Unexpected error occurred'}
        )