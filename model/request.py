from pydantic import BaseModel


class ReqModelLogin(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test",
                    "password": "test",
                }
            ]
        }
    }