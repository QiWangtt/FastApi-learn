# _*_ coding: utf-8 _*_
# @Time: 09.09.2024 13:54
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=6


import uvicorn
from fastapi import FastAPI, Path, Query, Body
from typing import Optional, List, Set
from pydantic import BaseModel, Field

app = FastAPI()


class Address(BaseModel):
    address: str
    postcode: str


# 对类里面的项目进行验证
class User(BaseModel):
    username: str = Field(..., min_length = 3) # ...表示这是一个必选项不是可选项
    description: Optional[str] = Field(None, max_length = 10) # None表示缺省值为空，如果给了输入参数，那么限制最大长度
    address: Address # 调用Adress类型


class Feature(BaseModel):
    name: str


class Item(BaseModel):
    name: str
    length: int
    features: List[Feature]


@app.put('/carts/{cart_id}')
async def update_cart(cart_id: int, user: User, item: Item, count: int = Body(..., ge = 2)): # 加上一个单一参数count的验证，限制count大于等于2
    print(user.username)
    print(item.name)
    result_dict ={
        "cart id": cart_id,
        "Username": user.username,
        "itemname": item.name,
        "count": count
    }
    return result_dict


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)

