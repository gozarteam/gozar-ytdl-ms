from pydantic import BaseModel, Field
from typing import Literal


class DownloadPayload(BaseModel):
    url: str
    format: Literal["best", "worst"] = Field(default="worst")
    noplaylist: bool = Field(default=True)
    geo_bypass: bool = Field(default=True)
