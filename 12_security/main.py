# _*_ coding: utf-8 _*_
# @Time: 12.09.2024 14:01
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=12
from datetime import datetime, timezone, timedelta
from os import access

import uvicorn
from anyio import get_current_task
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from typing import Optional, List, Set, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt


SECURITY_KEY = "drujfidftrg"
ARGORITHMS = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") # 这一句目前仍不理解


class Token(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()


# 验证用户名和密码
def validate_user(username: str, password: str):
    if username == 'jack' and password == '111':
      return username

    return None


def get_current_username(token: str = Depends(oauth2_scheme)):
    unauth_exp = HTTPException(status_code=401, detail="Unauthorized")
    try:
        username = None
        # 解码加密字符串, 解密出的内容是dict变量
        token_data = jwt.decode(token, SECURITY_KEY, ARGORITHMS)
        if token_data:
            # 解密成功，从dict变量中提取用户名
            username = token_data.get('username', None)
    # 如果发生异常
    except Exception as error:
        raise unauth_exp

    # 如果数据提取不成功，也报错
    if not username:
        raise unauth_exp

    # 如果都有了，就说明客户端发过来的token是有效的，那就返回用户名
    return username




@app.post('/token')
async def login(login_form: OAuth2PasswordRequestForm = Depends()):
    username = validate_user(login_form.username, login_form.password)
    if not username: # 如果用户名或者密码不存在就抛出下面异常
        raise HTTPException(status_code=401,
                            detail="Not authorized",
                            headers={"WWW-Authenticate": "Bearer"})

    # 如果存在，生成token， 并且设置10分钟过期
    token_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    token_data = {
        "username": username,
        "exp": token_expires
    }

    # 现在生成加密字符串, 需要传递要加密的数据， 密钥和算法
    token = jwt.encode(token_data, SECURITY_KEY, ARGORITHMS)
    return Token(access_token=token, token_type="bearer")


@app.get('/items') # 如果这里使用dependencies，则只能进行身份验证，但是无法获取其数据，比如验证之后使用其用户名， 所以这里不使用dependencies，而是在下面这句代码中使用Depends
async def get_items(username: str = Depends(get_current_username)): # 如果函数get_current_username验证token通过，那么这里就可以拿到用户名
    return {"current user": username}


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)
