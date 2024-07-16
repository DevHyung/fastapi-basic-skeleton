from pydantic import BaseModel


class ReqLogin(BaseModel):
    email: str = "hj.park@caredit.net"
    password: str = "password"
