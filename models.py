import uuid
from datetime import timedelta, datetime

from sqlalchemy import Column, Integer, Numeric, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), unique=True)
    password = Column(String(length=128))
    firstname = Column(String(length=128))
    lastname = Column(String(length=128))
    is_admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}," \
               f"username={self.username!r}," \
               f"firstname={self.firstname!r}," \
               f"lastname={self.lastname!r})," \
               f"is_admin={self.is_admin!r})"


class Salary(Base):
    __tablename__ = "salary"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    total = Column(Numeric)
    created_at = Column(DateTime, default=datetime.now())
    received_at = Column(DateTime, default=datetime.now() + timedelta(days=30))
    is_received = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Salary(id={self.id!r}," \
               f"employee_id={self.employee_id!r}," \
               f"total={self.total!r}," \
               f"created_at={self.created_at!r}," \
               f"received_at={self.received_at!r}," \
               f"is_received={self.is_received!r})"


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    created_at = Column(DateTime, default=datetime.now())
    received_at = Column(DateTime, default=datetime.now() + timedelta(days=30))
    is_received = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Promotion(id={self.id!r}," \
               f"employee_id={self.employee_id!r}," \
               f"created_at={self.created_at!r}," \
               f"received_at={self.received_at!r}," \
               f"is_received={self.is_received!r})"
