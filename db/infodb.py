#coding=utf-8
from __init__ import Article


def insert(article):
    Article.info.insert(article)


def save_pic(pic_list):
    Article.Image.insert(pic_list)


def get_Articles(skip, count):
    cur = Article.info.find().skip(skip).limit(count)
    return [i for i in cur]


def get_OneArticle(_id):
    return Article.info.find_one({"id": _id})


def get_OneImage(_id):
    return Article.Image.find_one({"id": _id})

if __name__ == "__main__":
    print len(get_Articles(0, 10))
