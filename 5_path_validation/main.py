# _*_ coding: utf-8 _*_
# @Time: 09.09.2024 12:43
# @Author: Qi Wang
# @File: main
# @Project: FastApi learn
# @Quelle: https://www.youtube.com/watch?v=n6Xa6cokCKc&list=PLvQDgAXJ4ADP4G8Iuc02B11bvFokZMChK&index=5
from idlelib.pathbrowser import PathBrowser

import uvicorn
from fastapi import FastAPI, Path, Query
from enum import Enum
from typing import Optional

app = FastAPI()

'''路径参数的验证'''

@app.get('/users')
# 1 is default value if there is no input for page_index
# alias是别名， 但是在python中不能使用-号链接字符串，会被认为是两个变量相减
async def get_users(page_index: int = Query(1, alias='page-index', title = 'Page Index', ge = 1, le = 1000)):
    return {'User': f'Index {page_index}'}


@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(..., title = 'User ID', ge = 12, le = 1000)): # gt: greater than; ge: greater and equal
    return {'User': f'This is the User for {user_id}'}


@app.get('/books/{book_name}')
async def get_books(book_name: str = Path(..., title = 'Book Name', min_length = 3, max_length = 30)): # 对字符串长度进行验证
    return {'Book Info': f'This is a book for {book_name}'}


@app.get('/items/{item_no}')
async def get_items(item_no: str = Path(..., title = 'Item No.', regex = '^[a|b|c]-[\\d]*$')): # 正则表达式，含义:必须是abc三个字母中的任何一个开头，然后加上"-数字"
    return {'Book Info': f'This is a book for {item_no}'}


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)
