from pydantic import BaseModel, ConfigDict
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    http_status_code: int
    additional_info: Optional[dict] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "An error occurred while processing your request",
                "error_code": "INTERNAL_SERVER_ERROR",
                "http_status_code": 500,
                "additional_info": {
                    "timestamp": "2023-05-20T12:34:56Z",
                    "request_id": "1234567890"
                }
            }
        }
    )