#coding=utf-8
from __init__ import Article

def insert(article):
    Article.info.insert(article)


def save_pic(pic_list):
    Article.Image.insert(pic_list)


def get_OneArticle(_id):
    return Article.info.find({"id": _id})


def get_OneImage():
    return Article.Image.find_one()

if __name__ == "__main__":
    print get_OneImage()
