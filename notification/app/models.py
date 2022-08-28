from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    notify: bool
    template: str
    email: str
    subject: str

class DataModel(BaseModel):
    template: str
    user_list: list[UserData]


