# _*_ coding: utf-8 _*_
# @Time: 09.09.2024 11:07
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=2

import uvicorn
from fastapi import FastAPI
from typing import Optional
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

class Gender(str, Enum): # Enum是枚举
    male = "male"
    female = "female"
    diverse = "diverse"

class UserModel(BaseModel):
    username: str
    description: Optional[str] = "default"
    gender: Gender


@app.post('/users')
async def create_user(user_model: UserModel):
    print(user_model.username)
    user_dict = user_model.model_dump()
    return user_dict

# 与路径参数混合使用
@app.put('/users/{user_id}') # 当需要修改用户的时候使用put
async def update_user(user_id:int, user_model: UserModel):
    print(user_model.username)
    user_dict = user_model.model_dump()
    user_dict.update({'id': user_id}) # 把user_id放到字典里面
    return user_dict


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)