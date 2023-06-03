from passlib.context import CryptContext
from sqlalchemy import desc
from sqlalchemy.orm import Session

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_own_salary(db: Session, employee_id: int):
    return db.query(models.Salary).filter_by(employee_id=employee_id).order_by(desc(models.Salary.id)).first()


def get_own_promotion(db: Session, employee_id: int):
    return db.query(models.Promotion).filter_by(employee_id=employee_id).order_by(desc(models.Promotion.id)).first()


def get_employee_by_username(db: Session, username: str):
    return db.query(models.Employee).filter_by(username=username).first()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    hashed_password = get_password_hash(employee.password)
    employee = models.Employee(firstname=employee.firstname, lastname=employee.lastname,
                               username=employee.username, password=hashed_password,
                               is_admin=employee.is_admin)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, user_id: int):
    return db.query(models.Employee).filter_by(id=user_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeCreate):
    db_employee = db.query(models.Employee).filter_by(id=employee_id).first()
    if not db_employee:
        return None
    if employee.firstname:
        db_employee.firstname = employee.firstname
    if employee.lastname:
        db_employee.lastname = employee.lastname
    if employee.username:
        db_employee.username = employee.username
    if employee.password:
        hashed_password = employee.password
        db_employee.password = hashed_password
    if employee.is_admin is not None:
        db_employee.is_admin = employee.is_admin
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(models.Employee).filter_by(id=employee_id).first()
    if not db_employee:
        return False
    db.delete(db_employee)
    db.commit()
    return True


# SALARIES
# CREATE
def create_salary(db: Session, salary: schemas.SalaryCreate):
    salary_db = models.Salary(employee_id=salary.employee_id,
                              total=salary.total,
                              received_at=salary.received_at,
                              is_received=salary.is_received)
    db.add(salary_db)
    db.commit()
    db.refresh(salary_db)
    return salary_db


# READ (ONE)
def get_salary(db: Session, salary_id: int):
    return db.query(models.Salary).filter_by(id=salary_id).first()


# READ (MANY)
def get_salaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Salary).offset(skip).limit(limit).all()


# UPDATE
def update_salary(db: Session, salary_id: int, salary: schemas.SalaryCreate):
    salary_db = db.query(models.Salary).filter_by(id=salary_id).first()
    if not salary_db:
        return None
    if salary.employee_id:
        salary_db.employee_id = salary.employee_id
    if salary.total:
        salary_db.total = salary.total
    if salary.received_at:
        salary_db.received_at = salary.received_at
    if salary.is_received is not None:
        salary_db.is_received = salary.is_received
    db.commit()
    db.refresh(salary_db)
    return salary_db


# DELETE
def delete_salary(db: Session, salary_id: int):
    salary_db = db.query(models.Salary).filter_by(id=salary_id).first()
    if not salary_db:
        return False
    db.delete(salary_db)
    db.commit()
    return True


# PROMOTIONS
# CREATE
def create_promotion(db: Session, promotion: schemas.PromotionCreate):
    promotion_db = models.Promotion(employee_id=promotion.employee_id,
                                    received_at=promotion.received_at,
                                    is_received=promotion.is_received)
    db.add(promotion_db)
    db.commit()
    db.refresh(promotion_db)
    return promotion_db


# READ (ONE)
def get_promotion(db: Session, promotion_id: int):
    return db.query(models.Promotion).filter_by(id=promotion_id).first()


# READ (MANY)
def get_promotions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Promotion).offset(skip).limit(limit).all()


# UPDATE
def update_promotion(db: Session, promotion_id: int, promotion: schemas.PromotionCreate):
    promotion_db = db.query(models.Promotion).filter_by(id=promotion_id).first()
    if not promotion_db:
        return None
    if promotion.employee_id:
        promotion_db.employee_id = promotion.employee_id
    if promotion.received_at:
        promotion_db.received_at = promotion.received_at
    if promotion.is_received is not None:
        promotion_db.is_received = promotion.is_received
    db.commit()
    db.refresh(promotion_db)
    return promotion_db


# DELETE
def delete_promotion(db: Session, promotion_id: int):
    promotion_db = db.query(models.Promotion).filter_by(id=promotion_id).first()
    if not promotion_db:
        return False
    db.delete(promotion_db)
    db.commit()
    return True
