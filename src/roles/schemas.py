from src.core.schemas import BaseSchema


class RoleSchema(BaseSchema):
    id: int
    code: str
    name: str


class RoleCreateSchema(BaseSchema):
    code: str
    name: str


class FunctionSchema(BaseSchema):
    id: int
    code: str
    version: int


class FunctionCreateSchema(BaseSchema):
    code: str
    version: int


class RoleFunctionsAssignSchema(BaseSchema):
    role_id: int
    function_ids: list[int]
