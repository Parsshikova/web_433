from fastapi import FastAPI

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    employees_count = Column(Integer)

Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

tom = User(name="Tom", age=38)
db.add(tom)

users = [
    User(name="Bob", age=42),
    User(name="Alice", age=33),
]
db.add_all(users)

companies = [
    Company(name="Yandex", employees_count=10000),
    Company(name="Microsoft", employees_count=200000),
]
db.add_all(companies)
db.commit()
print(tom.id)  
db.refresh(tom)
app = FastAPI()
