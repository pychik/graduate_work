from pydantic import BaseModel


class Template(BaseModel):
    body: str


class UserData(BaseModel):
    id: int
    notify: bool
    name: str
    message: str
    email: str


class DataModel(BaseModel):
    template: Template
    subject: str
    user_list: list[UserData]
