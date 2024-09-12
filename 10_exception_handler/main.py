# _*_ coding: utf-8 _*_
# @Time: 11.09.2024 13:09
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=10
from email import message_from_binary_file

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional, List, Set, Union

from jinja2 import TemplateRuntimeError
from pydantic import BaseModel, Field

from setuptools.command.alias import alias

Users = {
    # "x": {"id": 0},
    "a": {"id": 1, "username": "a"},
    "b": {"id": 2, "username": "b", "password": "bbb"},
    "c": {"id": 3, "username": "c", "password": "ccc", "description": "default"},
    "d": {"id": 4, "username": "d", "password": "ddd", "description": "User ddd"},
    "e": {"id": 5, "username": "e", "password": "eee", "description": "User eee", "fullname": "Mary Water"}
}

app = FastAPI()


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    fullname: Optional[str] = None
    description: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    ...


# 对于报错信息可以单独定义一个类
class ErrorMessage(BaseModel):
    error_code: int
    message: str


class UserNotFoundException(Exception):
    def __init__(self, username: str):
        self.username = username

# responses可以将异常内容的example values加入到api中，让用户看得到
@app.post('/users', status_code=201, response_model=UserOut, responses={
    400: {'model': ErrorMessage},
    401: {'model': ErrorMessage}
})
async def create_user(user: UserIn):
    if Users.get(user.username, None): # 这个if的用意在于，如果找到相同用户，则不能重复创建该用户，因此报错，错误码是400
        error_message = ErrorMessage(error_code=400, message=f'{user.username} already exists')
        return JSONResponse(status_code=400, content=error_message.model_dump())

    user_dict = user.model_dump()
    user_dict.update({"id": 10})

    return user_dict


# 如果找到了，状态码就是200，这是默认的，不写也可以
@app.get('/users/{username}', status_code=200, response_model=UserOut)
async def get_user(username: str = Path(..., min_length=1)): # username是一个路径参数， 这里要求最小长度1个字符， 这里对应Users里的a,b,c,d,e
    user = Users.get(username, None) # 从Users里面根据username找user， 如果没找到，返回None
    if user:
        return user # 如果找到了，返回user
    # 如果没找到，状态码等于404， 通过detail返回一句话 username notfound
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{username} not found')

    # 上面那句是fastapi标准异常报告 ,下面是自定义异常输入
    # fastapi发现某一个函数抛出了not found异常时， fastapi会执行下面user_not_found_exception_handler函数

    raise UserNotFoundException(username)


# 这里也是自定义异常的一部分
@app.exception_handler(UserNotFoundException) # 注意别选成handlers
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    # 当出现异常时，content里面是用户真正想返回的自定义内容
    return JSONResponse(status_code=404, content={
        'error_code': 404,
        'message': f'{exc.username} not found',
        'info': 'this is a test for errorreport',
        'advice': 'try to input a right username'
    })


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)