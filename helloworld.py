# _*_ coding: utf-8 _*_
# @Time: 04.09.2024 14:32
# @Author: Qi Wang
# @File: helloworld
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=aHRb8RoX9vI&list=PLFbd8KZNbe-_PWBT_L7V6fNYJOgER0ZlR&index=113

from fastapi import FastAPI

app = FastAPI()

@app.get("/helloworld")
async def hello_world():
    return {'message': 'Hello World'}
