from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class PaginationSchema(BaseSchema):
    limit: int = 20
    offset: int = 0
