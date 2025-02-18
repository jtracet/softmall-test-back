import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[..., Awaitable[Response]]) -> Response:
        start_time = time.time()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response
