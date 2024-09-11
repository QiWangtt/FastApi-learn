# _*_ coding: utf-8 _*_
# @Time: 11.09.2024 10:47
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=7

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Response
from typing import Optional, List, Set, Union
from pydantic import BaseModel, Field
from setuptools.command.alias import alias

app = FastAPI()


@app.put('/carts')
# Cookie和Header参数的名字不要使用下划线，如果变量名需要定义成下划线，那么通过alias来确保参数名没有下划线，alias是定义别名使用的
# Union表示参数可以是指定的数据类型的一种，相当于Optional的一种快捷方式
async def update_cart(*,
                      response: Response,
                      favorite_schema: Optional[str] = Cookie(None, alias="favorite-schema"),
                      api_token: Union[str, None] = Header(None, alias = "api-token")):
    result_dict ={
        "favorite_schema": favorite_schema,
        "api_token": api_token
    }

    response.set_cookie(key="favorite-schema", value="dark")

    return result_dict


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)