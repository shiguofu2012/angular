#coding=utf-8
from lxml import html
import uuid
import requests
import os
from tasks import downPic
from db.infodb import save_pic


def is_para(tag):
    if tag in ['p', 'br', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
        return True
    return False


def get_text(dom):
    if not isinstance(dom, html.HtmlElement):
        return ""
    if dom.tag in ['script', 'h1', 'h2', 'title']:
        return ""
    if dom.get("class") == "rich_media_meta_list":
        return ""
    is_paragraph = is_para(dom.tag)
    text = ""
    if dom.text:
        text += dom.text
    for d in dom:
        if d.tag == 'p':
            t = d.xpath('string(.)') + '\n'
        else:
            t = get_text(d)
        text += t
    if is_paragraph:
        text = text + '\n'
    return text


def validate_img(src):
    if not src:
        return False
    return True


def get_pic(dom):
    imgs = dom.findall(".//img")
    if not imgs:
        return []
    result = []
    for img in imgs:
        uid = uuid.uuid4()
        uid = ''.join(str(uid).split('-'))
        src = img.get("src")
        if not src:
            src = img.get("data-src")
        if validate_img(src):
            r = downPic.delay(src, uid)
            result.append({"id": uid, "node": img})
            save_pic({"id": uid})
    return result


if __name__ == "__main__":
    print downPic("http://mmbiz.qpic.cn/mmbiz/cTWzx3NVe32N649Bq0SAYhD0YXSg3d9yFhkYgMHY9ibHQvvmw9BfibOiczS78eRj8NPpd1EYZs3CzqTKiaWcm6f4mQ/640?wxfrom=100&tp=webp&wx_fmt=jpeg", "test")
