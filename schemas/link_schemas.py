from pydantic import BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    url: HttpUrl


class LinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_id: str
    original_url: str


class LinkStatsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_id: str
    clicks: int
