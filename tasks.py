#coding=utf-8
#!/usr/bin/python

from celery import Celery
from lxml import html
import urlparse
import requests
import os
import re
from db.infodb import update_pic, update_article, get_Newstemplate,\
        insert, save_link, get_OneImage
from process_article import get_pic, get_text
IMG_REP_STR = "<div>&ltpicturestart--%s--pictureend&gt</div>"
#URLPIC = "http://192.168.50.128/angular/picture/"
URLPIC = "http://192.168.1.113/angular/picture/"
PICDIR = "/home/gfshi/github/angular/picture"
DEFAULT_IMAGE = "http://192.168.1.113/angular/picture/default.jpg"
PATTERN_IMG = re.compile("&ltpicturestart--(.*?)--pictureend&gt")

app = Celery(
    "tasks",
    backend="redis://localhost:6379/2",
    broker="redis://localhost:6379/1")


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
        return None


def getQuery(url, parameter='__biz'):
    parse_result = urlparse.urlparse(url)
    query = parse_result.query
    q_dict = urlparse.parse_qs(query)
    return q_dict.get(parameter)[0]


def down_article(link, dynamic=False):
    if dynamic:
        out = os.popen("phantomjs down.js %s" % link)
        return out.read()
    else:
        r = requests.get(link)
        if r.ok:
            return r.content
        else:
            return None


def extract_item(dom, item, template, multi=False):
    if item not in template and not template.get(item):
        return ""
    item_value = dom.xpath(template[item])
    if multi:
        return item_value
    if item_value:
        return item_value[0]


def remove_tag(dom, xpath_str):
    xpath_str = "|".join(xpath_str.split("&"))
    tag_remove = dom.xpath(xpath_str)
    for tag in tag_remove:
        parent_node = tag.getparent()
        parent_node.remove(tag)


def extract(dom, template):
    article = {}
    tag_remove = template.get("remove", "")
    article['title'] = extract_item(dom, 'title', template)
    pubDate = extract_item(dom, "pubDate", template)
    article['pubDate'] = pubDate
    content = extract_item(dom, "content", template)
    text = ""
    remove_tag(content, tag_remove)
    pics = get_pic(content)
    for p in pics:
        node = p.pop("node")
        parent_node = node.getparent()
        parent_node.replace(node, html.fromstring(IMG_REP_STR % p.get("id")))
    text += get_text(content)
    text = text.replace("<", "&lt")
    text = text.replace(">", "&gt")
    article["content"] = text
    return article


@app.task
def downPic(url, name, isThumb=0):
    if not os.path.exists(PICDIR):
        os.makedirs(PICDIR)
    uid = name
    resp = requests.get(url)
    suffix = getSuffix(url)
    url = None
    if resp.ok:
        if not suffix:
            filepath = os.path.join(PICDIR, name)
        else:
            filepath = os.path.join(PICDIR, name + "." + suffix)
            name = name + "." + suffix
        f = open(filepath, "w")
        f.write(resp.content)
        f.close()
        url = URLPIC + name
    if isThumb:
        print update_article(uid, {"image": url})
    else:
        update_pic(uid, {"url": url})
    print url
    return url



def get_thumbnail(article):
    thum = PATTERN_IMG.search(article.get("content"))
    if not thum:
        return DEFAULT_IMAGE
    _id = thum.group(1)
    thum = get_OneImage(_id)
    if not thum:
        return DEFAULT_IMAGE
    return thum.get("url", DEFAULT_IMAGE)


@app.task
def downArticle(msg):
    if not isinstance(msg, dict):
        print 'parameters error!'
        return None
    _id = msg.get("_id")
    if not _id:
        print '_id is None'
    link = msg.get("linksource")
    article = down_article(link)
    dom = html.fromstring(article)
    biz = getQuery(link)
    if not biz:
        print "biz is Null"
        return
    templates = get_Newstemplate(biz)
    if not templates:
        print "templates is None"
        return
    article = extract(dom, templates[0])
    imageUrl = msg.get("picSource")
    msg.update(article)
    news_id = insert(msg)
    if imageUrl:
        downPic(imageUrl, _id, 1)
    else:
        image_url = get_thumbnail(article)
        update_article(_id, {"image": image_url})
    save_link({"link": link, "status": "OK", "id": news_id})


if __name__ == "__main__":
    getQuery("http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5NTM1NzEyMA==&uin=MTI3MjcwNjMyMA%3D%3D&key=77421cf58af4a65324c011322642b600d8aec931bbfb7c37cd376853a2a560b20c665aad57afffeae9ff172447b15b4d&devicetype=android-21&version=26031031&lang=zh_CN&nettype=WIFI&pass_ticket=mJ3n7Pdjld7jatCugVjmKsd6%2FET3dr%2F2t8s84sUvcjqBpOyd%2Fan5eWfJQufSfMzY")
