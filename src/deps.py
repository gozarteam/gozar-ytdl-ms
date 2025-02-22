from fastapi.security import APIKeyHeader
from fastapi import Depends
from fastapi.exceptions import HTTPException
from os import getenv


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
API_KEY = getenv("GYTDL_API_KEY", "123456789")


def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY and API_KEY is not None:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return api_key
