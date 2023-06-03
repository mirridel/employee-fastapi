from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class EmployeeBase(BaseModel):
    username: str
    firstname: Union[str, None] = None
    lastname: Union[str, None] = None
    is_admin: Union[bool, None] = None


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class SalaryBase(BaseModel):
    employee_id: int
    total: float
    received_at: Optional[datetime]
    is_received: Optional[bool] = False


class SalaryCreate(SalaryBase):
    pass


class Salary(SalaryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PromotionBase(BaseModel):
    employee_id: int
    received_at: Optional[datetime]
    is_received: Optional[bool] = False


class PromotionCreate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
