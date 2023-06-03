from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import crud
from models import Employee, Salary, Promotion


def fill_db(db: Session) -> bool:
    first_employee = Employee(username="username1",
                              password=crud.get_password_hash("password1"),
                              firstname="Elena",
                              lastname="Hoffman",
                              is_admin=True)
    second_employee = Employee(username="username2",
                               password=crud.get_password_hash("password2"),
                               firstname="Ivan",
                               lastname="Petrov",
                               is_admin=False)
    third_employee = Employee(username="username3",
                              password=crud.get_password_hash("password3"),
                              firstname="Sergey",
                              lastname="Pushkin",
                              is_admin=False)
    fourth_employee = Employee(username="username4",
                               password=crud.get_password_hash("password4"),
                               firstname="Anastasia",
                               lastname="Waltz",
                               is_admin=False)

    try:
        db.add_all([first_employee, second_employee, third_employee, fourth_employee])
        db.commit()
    except Exception as ex:
        print(ex)
        return False

    first_salary = Salary(employee_id=first_employee.id, total=1000)
    second_salary = Salary(employee_id=second_employee.id, total=300)
    third_salary = Salary(employee_id=third_employee.id, total=2000)
    fourth_salary = Salary(employee_id=third_employee.id, total=500)

    try:
        db.add_all([first_salary, second_salary, third_salary, fourth_salary])
        db.commit()
    except Exception as ex:
        print(ex)
        return False

    first_promotion = Promotion(employee_id=second_employee.id, received_at=datetime.now() + timedelta(days=60))
    second_promotion = Promotion(employee_id=third_employee.id, received_at=datetime.now() + timedelta(days=14))

    try:
        db.add_all([first_promotion, second_promotion])
        db.commit()
    except Exception as ex:
        print(ex)
        return False
    db.close()
    return True
