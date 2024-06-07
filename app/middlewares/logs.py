from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logging_configs import logger


class LogsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging incoming requests and completed responses.

    This middleware logs details about incoming requests and completed responses
    using the configured logger.

    Args:
        app: The ASGI application.
        some_attribute (str): Some attribute required for middleware initialization.

    Attributes:
        some_attribute (str): Some attribute passed during initialization.

    Note:
        This middleware should be registered using `app.add_middleware(LogsMiddleware)`.
    """

    def __init__(self, app, some_attribute: str):
        """
        Initializes the LogsMiddleware.

        Args:
            app: The ASGI application.
            some_attribute (str): Some attribute required for middleware initialization.
        """
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        """
        Dispatch method to handle incoming requests and completed responses.

        This method logs details about incoming requests and completed responses
        using the configured logger.

        Args:
            request (Request): The incoming HTTP request object.
            call_next (Callable): The callback function to proceed with the request.

        Returns:
            Response: The HTTP response returned by the next middleware or endpoint.
        """
        logger.info(f"Received request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Completed response: {response.status_code}")
        return response
