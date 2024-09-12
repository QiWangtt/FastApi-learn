# _*_ coding: utf-8 _*_
# @Time: 12.09.2024 09:33
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=2

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from typing import Optional, List, Set, Union

from jinja2 import TemplateRuntimeError
from pydantic import BaseModel, Field

from setuptools.command.alias import alias


async def set_charset():
    print("set UTF-8")

# 如果在定义api的app之初就添加dependencies，那么后续定义的所有api被执行时都会调用依赖的对象
# 这叫做全局dependencies依赖
app = FastAPI(dependencies=[Depends(set_charset)])

# 验证api_token是否正确，哪些api的调取如果需要token验证，就把这个api设为依赖下面这个函数
async def verify_auth(api_token: Optional[str]=Header(None, alias="api-token")):
    if not api_token:
        # 如果错误，哪么使用者无权调取api
        raise HTTPException(status_code=400, detail="Unauthorized")


def total_param(total_page: Optional[int] = 1):
    return total_page


# 依赖注入
# 首先是函数作为依赖项
def pageinfo_params(page_index: Optional[int] = 1, page_size: Optional[int] = 10,
                    total: Optional[int] = Depends(total_param)): # 函数可以依赖另一个函数
    return {"page_index": page_index, "page_size": page_size, "total": total}


# 其次还可以使用类作为依赖项
class PageInfo:
    def __init__(self, page_index: Optional[int] = 1, page_size: Optional[int] = 10,
                 total: Optional[int] = Depends(total_param)):
        self.page_index = page_index
        self.page_size = page_size
        self.total = total


@app.get('/items')
async def get_items(page_info: dict = Depends(pageinfo_params)): # Depends相当于把函数pageinfo_params的返回值作为一个整体放在page_info里

    return {"page_index": page_info.get("page_index"),
            "page_size": page_info.get("page_size"),
            "total": page_info.get("total") # 这里可以调取total，因为子函数pageinfo_params本身也依赖另一个函数total_param
            }


@app.get('/users', dependencies=[Depends(verify_auth)]) # 这里是设置get users这个api的调用时依赖于token验证的
# 使用Depends可以实现代码复用，不必在api函数体内再次定义。这里的示例是依赖class注入
# 当把class作为依赖项时，class PageInfo会构造一个对象传给page_info，所以要把dict改成对象名PageInfo
async def get_users(page_info: PageInfo = Depends(PageInfo)):
    # 作为对象类型就不能使用get了，直接加点.选择参数名即可
    return {"page_index": page_info.page_index, "page_size": page_info.page_size, "total": page_info.total}


@app.get('/goods')
async def get_users(page_info: PageInfo = Depends()): # 因为PageInfo是class，当这样写Depends时，就会自动识别class，括号内不需要再写PageInfo了

    return {"page_index": page_info.page_index, "page_size": page_info.page_size, "total": page_info.total}


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)
