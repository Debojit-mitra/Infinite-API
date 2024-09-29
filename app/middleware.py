import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import traceback
import json

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log detailed error information
            error_details = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "request_method": request.method,
                "request_url": str(request.url),
                "request_headers": dict(request.headers),
                "request_query_params": dict(request.query_params),
                "traceback": traceback.format_exc()
            }
            
            # Try to include request body, if possible
            try:
                body = await request.json()
                error_details["request_body"] = body
            except:
                error_details["request_body"] = "Unable to parse request body"

            logger.error(f"An error occurred while processing the request: {json.dumps(error_details, indent=2)}")

            # Return a generic error response to the client
            return Response(
                content=json.dumps({"error": "An internal server error occurred"}),
                status_code=500,
                media_type="application/json"
            )