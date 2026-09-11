import os
from dataclasses import dataclass
from typing import Literal, cast


@dataclass(frozen=True)
class Settings:
    environment: Literal["development", "test", "production"] = "development"

    @classmethod
    def from_env(cls) -> "Settings":
        environment = os.getenv("APP_ENV", "development")
        if environment not in {"development", "test", "production"}:
            raise ValueError("APP_ENV must be development, test, or production")
        return cls(environment=cast(Literal["development", "test", "production"], environment))
