
from sqlalchemy import create_engine, engine, Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///nuage.db")
Base = declarative_base()

class AttendanceLog(Base):
    __tablename__ = 'attendance_log'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    student_id = Column(Integer)
    present = Column(Integer)
    submitted_by = Column(String(50))
    updated_at = Column(TIMESTAMP)


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(100))
    department_id = Column(Integer)
    semester = Column(Integer)
    c_class = Column(String)
    lecture_hours = Column(Integer)
    submitted_by = Column(String(100))
    updated_at = Column(TIMESTAMP)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    type = Column(String(100))
    full_name = Column(String(100))
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    submitted_by = Column(String(100))
    updated_at = Column(TIMESTAMP)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department_name = Column(String(100))
    submitted_by = Column(String(100))
    updated_at = Column(TIMESTAMP)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    department_id = Column(Integer)
    st_class = Column(String(100))
    submitted_by = Column(String(100))
    updated_at = Column(TIMESTAMP)




