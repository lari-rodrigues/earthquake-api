from pydantic import BaseModel, Field

class CityRequest(BaseModel):
    name: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    country: str= Field(..., min_length=1)