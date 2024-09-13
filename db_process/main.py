# _*_ coding: utf-8 _*_
# @Time: 13.09.2024 09:21
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=13

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, String, Integer, select, asc
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass


engine = create_engine('fg', echo=True)


# Define database models， 准备一张数据库的表
class StudentEntity(Base):
    __tablename__="student"

    # id影射Integer
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # name影射String， 且规定其长度最大为128位, 不能有重复，且String不能为空
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)



Base.metadata.create_all(engine) # 当程序执行到这里时， 就会根据上面的影射，创建出student表
Session = sessionmaker(bind=engine)
app = FastAPI()


# Define API models


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)


