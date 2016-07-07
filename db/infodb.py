#coding=utf-8
from . import Article

def insert(article):
    Article.info.insert(article)


def save_pic(pic_list):
    Article.Image.insert(pic_list)


def get_OneArticle(_id):
