# _*_ coding: utf-8 _*_
# @Time: 09.09.2024 09:39
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=2
from winreg import EnumKey

import uvicorn
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class Gender(str, Enum): # Enum是枚举
    male = "male"
    female = "female"
    diverse = "diverse"

# 对于@app.get，小范围在前，大范围在后， current是固定字符串，属于小范围
@app.get('/users/current')
async def get_current_user():
    return {'user': f'This is current user'}


@app.get('/users/{user_id}')
async def get_user(user_id: int):
    return {'user': f'This is the user for {user_id}'}


@app.get('/students/{gender}')
async def get_user(gender: Gender): # Gender 是上面定义的性别枚举类
    return {'student': f'This is a {gender.value} student'}


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)

