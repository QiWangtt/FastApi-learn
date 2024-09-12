# _*_ coding: utf-8 _*_
# @Time: 11.09.2024 11:16
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=9

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response
from typing import Optional, List, Set, Union

from pydantic import BaseModel, Field
from pygments.lexer import default
from setuptools.command.alias import alias

Users = {
    "x": {"id": 0},
    "a": {"id": 1, "Username": "a"},
    "b": {"id": 2, "Username": "b", "password": "bbb"},
    "c": {"id": 3, "Username": "c", "password": "ccc", "description": "default"},
    "d": {"id": 4, "Username": "d", "password": "ddd", "description": "User ddd"},
    "e": {"id": 5, "Username": "e", "password": "eee", "description": "User eee", "fullname": "Mary Water"}
}

app = FastAPI()


class UserOut(BaseModel):
    id: int
    Username: str # 如果User中不包含 Username就会报错
    description: Optional[str] = "default" # 使用Optional就不会报错

# response_model告诉fastapi，函数输出的结果使用这个模型的内容，相当于执行过滤，把不要的信息过滤掉
# response_model_include相当于再次过滤，只输出UserOut模型中的部分内容
# @app.get('/Users/{Username}', 9_response_model=UserOut, response_model_include={"id"})

# response_model_exclude相当于再次过滤，要求某项内容不要输出，剩余内容输出
# @app.get('/Users/{Username}', 9_response_model=UserOut, response_model_exclude={"id"})

# response_model_exclude_unset: 当User里面某个值没有设定就不输出该值，
@app.get('/Users/{Username}', response_model=UserOut, response_model_exclude_unset=True)
# 下面这行，如果不使用response_model，则Swagger UI会直接输出Users对应Username的全部内容
# @app.get('/Users/{Username}')
async def get_User(Username: str):
    return Users.get(Username, {})


# 下面这三行代码用于获取Users全部数据，但是没有运行成功
# @app.get('/Users', 9_response_model= List[UserOut])
# async def get_users():
#     return Users.values()


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)