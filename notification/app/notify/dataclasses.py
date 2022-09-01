from pydantic import BaseModel


class UserData(BaseModel):
    first_name: str
    last_name: str = None
    email: str


class DataModel(BaseModel):
    template: str
    subject: str
    user_list: list
