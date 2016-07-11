#coding=utf-8
from lxml import html
import uuid
import requests
import os
PICDIR = "/home/gfshi/github/angular/picture"
URLPIC = "http://192.168.50.128/angular/picture/"


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


def getSuffix(url):
    url_list = url.split("/")
    last = url_list[len(url_list) - 1]
    index = last.find(".")
    if index != -1:
        return url[index + 1:]
    index = last.find("wx_fmt")
    if index != -1:
        return last[index + 7:]
    else:
        print url
        return None


def downPic(url, name):
    resp = requests.get(url)
    suffix = getSuffix(url)
    if resp.ok:
        if not suffix:
            filepath = os.path.join(PICDIR, name)
        else:
            filepath = os.path.join(PICDIR, name + "." + suffix)
            name = name + "." + suffix
        f = open(filepath, "w")
        f.write(resp.content)
        f.close()
        return URLPIC + name
    else:
        return None


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
            pic = downPic(src, uid)
            result.append({"id": uid, "url": pic, "node": img})
    return result


if __name__ == "__main__":
    print downPic("http://mmbiz.qpic.cn/mmbiz/cTWzx3NVe32N649Bq0SAYhD0YXSg3d9yFhkYgMHY9ibHQvvmw9BfibOiczS78eRj8NPpd1EYZs3CzqTKiaWcm6f4mQ/640?wxfrom=100&tp=webp&wx_fmt=jpeg", "test")
