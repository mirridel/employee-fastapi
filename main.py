from datetime import datetime, timedelta
from typing import Union, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from sqlalchemy.orm import Session

import crud
import schemas
import settings

"""
+ docker
+ тесты
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_db():
    db = settings.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db, username: str, password: str):
    user = crud.get_employee_by_username(db, username)
    if not user:
        return False
    if not crud.verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_employee_by_username(db=db, username=token_data.username)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.Employee = Depends(get_current_user)):
    return current_user


async def get_current_admin_user(current_user: schemas.Employee = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


@app.post("/token", response_model=schemas.Token, tags=["user"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.Employee, tags=["user"])
async def read_users_me(current_user: schemas.Employee = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/salary/", response_model=schemas.Salary, tags=["user"])
async def read_own_salary(current_user: schemas.Employee = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    own_salary = crud.get_own_salary(db, current_user.id)
    if not own_salary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary not found",
        )
    return own_salary


@app.get("/users/me/promotion/", response_model=schemas.Promotion, tags=["user"])
async def read_own_promotion(current_user: schemas.Employee = Depends(get_current_active_user),
                             db: Session = Depends(get_db)):
    own_promotion = crud.get_own_promotion(db, current_user.id)
    if not own_promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion not found",
        )
    return own_promotion


# ADMIN
# EMPLOYEES
# CREATE
@app.post("/admin/employees/", response_model=schemas.Employee, tags=["admin"])
def create_employee(employee: schemas.EmployeeCreate,
                    current_user: schemas.Employee = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_username(db, username=employee.username)
    if db_employee:
        raise HTTPException(status_code=400,
                            detail="Username already registered")
    return crud.create_employee(db, employee=employee)


# READ (MANY)
@app.get("/admin/employees/", response_model=List[schemas.Employee], tags=["admin"])
def read_employees(skip: int = 0, limit: int = 100,
                   current_user: schemas.Employee = Depends(get_current_admin_user),
                   db: Session = Depends(get_db)):
    return crud.get_employees(db, skip, limit)


# READ (ONE)
@app.get("/admin/employees/{employee_id}", response_model=schemas.Salary, tags=["admin"])
def read_employee(employee_id: int, current_user: schemas.Employee = Depends(get_current_admin_user),
                  db: Session = Depends(get_db)):
    user = crud.get_employee(db=db, user_id=employee_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return user


# UPDATE
@app.put("/admin/employees/{employee_id}", response_model=schemas.Employee, tags=["admin"])
def update_employee(employee_id: int, employee: schemas.EmployeeCreate,
                    current_user: schemas.Employee = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db=db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


# DELETE
@app.delete("/admin/employees/{employee_id}", tags=["admin"])
def delete_employee(employee_id: int, current_user: schemas.Employee = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db=db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted"}


# SALARIES
# CREATE
@app.post("/admin/salaries/", response_model=schemas.Salary, tags=["admin"])
def create_salary(salary: schemas.SalaryCreate, current_user: schemas.Employee = Depends(get_current_admin_user),
                  db: Session = Depends(get_db)):
    return crud.create_salary(db=db, salary=salary)


# READ (MANY)
@app.get("/admin/salaries/", response_model=List[schemas.Salary], tags=["admin"])
def read_salaries(skip: int = 0, limit: int = 100, current_user: schemas.Employee = Depends(get_current_admin_user),
                  db: Session = Depends(get_db)):
    return crud.get_salaries(db=db, skip=skip, limit=limit)


# READ (ONE)
@app.get("/admin/salaries/{salary_id}", response_model=schemas.Salary, tags=["admin"])
def read_salary(salary_id: int, current_user: schemas.Employee = Depends(get_current_admin_user),
                db: Session = Depends(get_db)):
    salary = crud.get_salary(db=db, salary_id=salary_id)
    if salary is None:
        raise HTTPException(status_code=404, detail="Salary not found")
    return salary


# UPDATE
@app.put("/admin/salaries/{salary_id}", response_model=schemas.Salary, tags=["admin"])
def update_salary(salary_id: int, salary: schemas.SalaryCreate,
                  current_user: schemas.Employee = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    salary_updated = crud.update_salary(db=db, salary_id=salary_id, salary=salary)
    if salary_updated is None:
        raise HTTPException(status_code=404, detail="Salary not found")
    return salary_updated


# DELETE
@app.delete("/admin/salaries/{salary_id}", tags=["admin"])
def delete_salary(salary_id: int, current_user: schemas.Employee = Depends(get_current_admin_user),
                  db: Session = Depends(get_db)):
    salary_deleted = crud.delete_salary(db=db, salary_id=salary_id)
    if not salary_deleted:
        raise HTTPException(status_code=404, detail="Salary not found")
    return {"detail": "Salary deleted"}


# PROMOTIONS
# CREATE
@app.post("/promotions/", response_model=schemas.Promotion, tags=["admin"])
def create_promotion(promotion: schemas.PromotionCreate,
                     current_user: schemas.Employee = Depends(get_current_admin_user),
                     db: Session = Depends(get_db)):
    return crud.create_promotion(db=db, promotion=promotion)


# READ (MANY)
@app.get("/admin/promotions/", response_model=List[schemas.Promotion], tags=["admin"])
def read_promotions(skip: int = 0, limit: int = 100,
                    current_user: schemas.Employee = Depends(get_current_admin_user),
                    db: Session = Depends(get_db)):
    return crud.get_promotions(db=db, skip=skip, limit=limit)


# READ (ONE)
@app.get("/promotions/{promotion_id}", response_model=schemas.Promotion, tags=["admin"])
def read_promotion(promotion_id: int, current_user: schemas.Employee = Depends(get_current_admin_user),
                   db: Session = Depends(get_db)):
    promotion = crud.get_promotion(db=db, promotion_id=promotion_id)
    if promotion is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion


# UPDATE
@app.put("/promotions/{promotion_id}", response_model=schemas.Promotion, tags=["admin"])
def update_promotion(promotion_id: int, promotion: schemas.PromotionCreate,
                     current_user: schemas.Employee = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    promotion_updated = crud.update_promotion(db=db, promotion_id=promotion_id, promotion=promotion)
    if promotion_updated is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion_updated


# DELETE
@app.delete("/promotions/{promotion_id}", tags=["admin"])
def delete_promotion(promotion_id: int, current_user: schemas.Employee = Depends(get_current_admin_user),
                     db: Session = Depends(get_db)):
    promotion_deleted = crud.delete_promotion(db=db, promotion_id=promotion_id)
    if not promotion_deleted:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return {"detail": "Promotion deleted"}
