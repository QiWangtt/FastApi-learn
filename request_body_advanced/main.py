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
    address: str = Field(..., examples=["5 Queens Street"]) # 1. 通过Field设定 example数据，最值得推荐的方法
    postcode: str = Field(..., examples=["0765"])


    '''2. 直接用model_config也可以设定示例数据'''
    model_config = {
        "json_schema_extra":{
            "examples":[{
                "adress": "2 Queens Street",
                "Postcode": "0987"
            }]
        }
    }


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


# python基础，加了*号之后必须使用关键字传参， 示例
# def add(*, num1: int, num2: int):
#     return num1 + num2
#
# print(add(num1=1, num2=2))


@app.put('/carts/{cart_id}')
# 加上一个单一参数count的验证，限制count大于等于2
# 3. 在body内部也可以设定示例参数
# 三种方法优先级 model_config > Field > Body， 其中Field方法适合维护，如果不需要某参数，直接在Field中删除一次就行
async def update_cart(cart_id: int, user: User, item: Item, count: int = Body(..., ge = 2, examples=[8])):
# 在函数体内加上*号表示函数内的参数变成关键字参数，没有位置参数了，传参时必须用关键字传参
# async def update_cart(*, cart_id: int, user: User = Body(..., examples=[{"Username": "Smith"}]), item: Item, count: int = Body(..., ge = 2, examples=[8])):
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

