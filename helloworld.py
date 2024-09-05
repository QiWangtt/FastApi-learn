# _*_ coding: utf-8 _*_
# @Time: 05.09.2024 09:25
# @Author: Qi Wang
# @File: helloworld
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=aHRb8RoX9vI&list=PLFbd8KZNbe-_PWBT_L7V6fNYJOgER0ZlR&index=113
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello_world2():
    return {'message': 'Hello Wohgrld2'}

@app.get("/helloworld")
async def hello_world():
    return {'message': 'Hellocvgb c World'}



# 下面这条指令是在terminal或者cmd窗口运行的， 即使用uvicorn这个ASGI服务器组件启动API
# 'reload' means the programm will restart automatically after new savings
# uvicorn helloworld:app --reload

# 但是也可以在程序内部自动运行，例如:
if __name__ == '__main__':
    uvicorn.run("hello_world:app", reload=True)
