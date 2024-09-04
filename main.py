# _*_ coding: utf-8 _*_
# @Time: 04.09.2024 14:07
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=aHRb8RoX9vI&list=PLFbd8KZNbe-_PWBT_L7V6fNYJOgER0ZlR&index=113

from typing import Optional

import uvicorn
from fastapi import FastAPI

app = FastAPI
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

uvicorn.run(app, host="0.0.0.0", port=8000)