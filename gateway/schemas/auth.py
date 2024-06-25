import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class Gender(str, Enum):
    male = "M"
    female = "F"


class Roles(str, Enum):
    candidate = "candidate"
    hr = "hr"


class SignUp(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    gender: Gender
    telegram: str
    birthday: str = '01.01.1980'
    city: int
    job_city: int
    grade: int
    role: Roles


class SignIn(BaseModel):
    email: str
    password: str


class RestorePassword(BaseModel):
    password: str
    new_password: str
