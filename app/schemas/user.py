from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "Cashier"


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    role: str | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str