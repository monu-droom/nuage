from fastapi import FastAPI, status, requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from database import Base, engine, AttendanceLog, Course, User, Department, Student
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from logging.config import dictConfig
from log_config import log_config
import logging
from passlib.context import CryptContext

class AttendanceLogRequest(BaseModel):
    student_id: int
    course_id: int
    present: int
    submitted_by: str

class CourseRequest(BaseModel):
    course_name: str
    department_id: int
    semester: int
    c_class: str
    lecture_hours: int
    submitted_by: str  

class UserRequest(BaseModel):
    type: str
    full_name: str
    username: str
    email: str
    password: str
    submitted_by: str

class DepartmentRequest(BaseModel):
    department_name: str
    submitted_by: str

class StudentRequest(BaseModel):
    full_name: str
    department_id: int
    st_class: str
    submitted_by: str

Base.metadata.create_all(engine)

app = FastAPI(debug=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event('startup')
async def startup_event():
    db_session = Session(bind=engine, expire_on_commit=False)
    user_db = User(type='admin', full_name='Admin Corp', username='admincorp12', email='admin@corp.com', password=pwd_context.hash("123456"), submitted_by='admin')
    db_session.add(user_db)
    db_session.commit()
    db_session.close()
    logger = logging.getLogger('foo-logger')
    logger.debug(f'Username is admincorp12 and password is 123456')
    return {"status":"success", "msg":"User created successfully."}


@app.get('/')
def root():
    logger = logging.getLogger('foo-logger')
    logger.debug('This is test')

@app.post('/user', status_code=status.HTTP_201_CREATED)
def add_user(user: UserRequest):
    db_session = Session(bind=engine, expire_on_commit=False)
    user_db = User(type=user.type, full_name=user.full_name, username=user.username, email=user.email, password=pwd_context.hash(user.password), submitted_by=user.submitted_by)
    db_session.add(user_db)
    db_session.commit()
    db_session.close()
    
    return {"status":"success", "msg":"User created successfully."}

@app.get('/user/{id}')
def get_user_by_id(id:int):
    db_session = Session(bind=engine, expire_on_commit=False)
    user = db_session.query(User).filter(User.id==id).all()
    db_session.commit()
    db_session.close()

    return {"status":"success", "data":user}

@app.put('/user/{id}')
def update_user_by_id(id:int, type:str, full_name:str, username:str, email:str, password:str, submitted_by:str):
    db_session = Session(bind=engine, expire_on_commit=False)
    user = db_session.query(user).get(id)

    if user:
        user.type = type
        user.full_name = full_name
        user.username = username
        user.email = email
        user.password = pwd_context.hash(password)
        user.submitted_by = submitted_by

    db_session.commit()
    db_session.close()

    return {"status":"success", "data":user}

@app.delete('/user/{id}')
def delete_user(id:int):
    db_session = Session(bind=engine, expire_on_commit=False)
    user = db_session.query(User).filter(User.id==id).delete()
    db_session.commit()
    db_session.close()
    
    return {"status":"success", "msg":"User has been deleted successfully."}


@app.post('/course', status_code=status.HTTP_201_CREATED)
def add_user(course: UserRequest):
    db_session = Session(bind=engine, expire_on_commit=False)
    course_db = Course(course_name=course.course_name, department_id=course.department_id, semester=course.semester, c_class=course.c_class, lecture_hours=course.lecture_hours, submitted_by=course.submitted_by)
    db_session.add(course_db)
    db_session.commit()
    db_session.close()
    
    return {"status":"success", "msg":"Course added successfully."}


@app.post('/student', status_code=status.HTTP_201_CREATED)
def add_user(student: StudentRequest):
    db_session = Session(bind=engine, expire_on_commit=False)
    student_db = Student(full_name=student.full_name, department_id=student.department_id, st_class=student.st_class, submitted_by=student.submitted_by)
    db_session.add(student_db)
    db_session.commit()
    db_session.close()
    
    return {"status":"success", "msg":"Student added successfully."}


@app.post('/department', status_code=status.HTTP_201_CREATED)
def add_user(department: StudentRequest):
    db_session = Session(bind=engine, expire_on_commit=False)
    department_db = Department(department_name=department.department_name, submitted_by=department.submitted_by)
    db_session.add(department_db)
    db_session.commit()
    db_session.close()
    
    return {"status":"success", "msg":"Department added successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, log_level="debug", reload=False,)




