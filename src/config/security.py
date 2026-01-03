from datetime import timedelta

from pydantic import BaseModel


class SecurityConfig(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXP_MINUTES: int
    REFRESH_EXP_DAYS: int

    @property
    def access_exp_delta(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_EXP_MINUTES)

    @property
    def refresh_exp_delta(self) -> timedelta:
        return timedelta(days=self.REFRESH_EXP_DAYS)
