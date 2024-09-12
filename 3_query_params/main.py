# _*_ coding: utf-8 _*_
# @Time: 09.09.2024 10:27
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=3


import uvicorn
from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()


# 下面这个@app.get必须输入两个参数
# @app.get('/users')
# async def get_users(page_index: int, page_size: int):
#     return {'page info': f'index: {page_index}, size: {page_size}'}


# 下面这个可以不必全部输入，如果不输入则会默认输出缺省值
@app.get('/users')
async def get_users(page_index: int, page_size: Optional[int] = 30):
    return {'page info': f'index: {page_index}, size: {page_size}'}

# 路径参数和查询参数混合
@app.get('/users/{user_id}/friends') # 这一行是路径参数
# 只要下面这一行的参数列表里的参数没有出现在路径参数中，那它就是查询参数
async def get_user_friends(page_index: int, user_id: int, page_size: Optional[int] = 10):
    return {'user friends': f'user id: {user_id}, index: {page_index}, size: {page_size}'}


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)

