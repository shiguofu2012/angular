#coding=utf-8
from __init__ import Article


def insert(article):
    Article.info.insert(article)


def save_pic(pic_list):
    Article.image.insert(pic_list)


def update_pic(_id, data):
    return Article.image.update({"id": _id}, {"$set": data})


def get_Articles(skip, count):
    cur = Article.info.find().sort([("_id", -1)]).skip(skip).limit(count)
    return [i for i in cur]


def get_OneArticle(_id):
    return Article.info.find_one({"_id": _id})


def get_OneImage(_id):
    return Article.image.find_one({"id": _id})


def get_ImageByCond(cond):
    cur = Article.image.find(cond)
    return [i for i in cur]

if __name__ == "__main__":
    print len(get_Articles(0, 10))
