#coding=utf-8
from lxml import html
import uuid


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
        src = img.get("src")
        if not src:
            src = img.get("data-src")
        if validate_img(src):
            result.append({"id": uid, "url": src, "node": img})
    return result
