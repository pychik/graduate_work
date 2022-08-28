from pydantic import BaseModel


class DataModel(BaseModel):
    template: str
    user_list: list[UserData]


class UserData(BaseModel):
    id: int
    notify: bool
    template: str
    email: str
    subject: str