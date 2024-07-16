from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from os import path, environ, getenv
from typing import Literal


""" CONFIG AREA ===== START """
parent_path = path.abspath(path.join(path.abspath(__file__), "../../")) # 1-depth above == ../../
MODE: Literal["DEV", "PROD"] = "DEV"
""" CONFIG AREA ===== END """


@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = path.dirname(path.dirname(path.abspath(__file__)))
    NAVER_CLIENT_ID: str = getenv('NAVER_CLIENT_ID')
    NAVER_CLIENT_SECRET: str = getenv('NAVER_CLIENT_SECRET')
    SECRET_KEY: str = getenv('SECRET_KEY')
    DATABASE_URL = getenv('DATABASE_URL')


@dataclass
class LocalConfig(Config):
    TYPE: str = "DEV"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # DEV 60, PROD 15
    PROJ_RELOAD: bool = True


@dataclass
class ProdConfig(Config):
    TYPE: str = "PROD"
    # 15 minutes * 0 hours * 0 days = 15 min
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # DEV 60, PROD 15
    PROJ_RELOAD: bool = False


def conf(mode: Literal["DEV", "PROD"] = "DEV") -> LocalConfig | ProdConfig:
    global  parent_path

    load_dotenv(dotenv_path=path.join(parent_path, ".env"))

    config = dict(
        PROD=ProdConfig(),
        DEV=LocalConfig()
    )

    return config.get(environ.get("API_ENV", mode))


if __name__ == "__main__":
    print(asdict(LocalConfig()))
    print(conf().BASE_DIR)
else:
    CONFIG = conf(mode=MODE)
