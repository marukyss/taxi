from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int

    username: str
    token: str

    balance: float
    committed_trips: int


class UserSchemaCreate(BaseModel):
    username: str
    password: str
