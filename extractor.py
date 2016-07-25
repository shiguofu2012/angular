#!/usr/bin/python
from lxml import html
from process_article import get_text
from tasks import downPic, downArticle
from db.infodb import insert, save_pic, get_OneImage, getOnelink
import requests
import uuid
import time
import os
import sys
import re

pub_templat = {
        "block": "//div[@class=\"msg_list_bd\"]",
        "subblock": ".//div[@class=\"sub_msg_list\"]",
        "time": ".//p[@class=\"msg_date\"]",
        "title": ".//h4[@class=\"msg_title\"]/text()",
        "link": ".//a[@class=\"sub_msg_item redirect\"]/@hrefs",
        "picture": [".//span[@class=\"thumb\"]/img/@data-src", ".//span[@class=\"thumb\"]/img/@data-src"],
        "domain": "mp.weixin.qq.com"
        }

weixin_templat = {
        "block": "//ul[@id=\"pc_0_subd\"]",
        "subblock": ".//li",
        "time": ".//span[@class=\"sc\"]",
        "link": ".//h4/a/@href",
        "title": ".//h4/a/text()",
        "picture": ".//div[@class=\"wx-img-box\"]/a/img/@src",
        }


newsTemplate = {
        "title": "//h2/text()",
        "content": "//div[@id=\"img-content\"]",
        "pubDate": ".//em[@id=\"post-date\"]/text()",
        "remove": ".//section[@label=\"powered by 135editor.com\"]/p[position() > last() - 18]&.//div[@class=\"rich_media_tool\"]",
        "__biz": "MjM5NTM1NzEyMA=="
        }


def validateUrl(url):
    if url.startswith("http") or url.startswith("https"):
        return True
    return False


def extract_link(dom, template):
    result = []
    blocks = dom.xpath(template["block"])
    for block in blocks:
        t = block.xpath(template['time'])
        articles = block.xpath(template['subblock'])
        for a in articles:
            title = a.xpath(template['title'])
            if title and isinstance(title, list):
                title = title[0]
            link = a.xpath(template['link'])
            if link and isinstance(link, list):
                link = link[0]
            if not link:
                continue
            crawled = getOnelink(link)
            if crawled:
                continue
            pic_temps = template['picture']
            name = uuid.uuid4()
            name = ''.join(str(name).split("-"))
            tmp = {}
            tmp['title'] = title
            tmp['linksource'] = link
            tmp['_id'] = name
            for t in pic_temps:
                pic = a.xpath(t)
                if pic and isinstance(pic, list):
                    pic = pic[0]
                    if validateUrl(pic):
                        tmp['picSource'] = pic
                if pic:
                    break
            downArticle.delay(tmp)
            result.append(tmp)
    return result


def open_file(filename):
    f = open(filename)
    content = f.read()
    f.close()
    dom = html.fromstring(content)
    return dom


def add_template(temp):
    import pymongo
    client = pymongo.MongoClient()
    db = client.infos
    db.newsTemplate.insert(temp)



if __name__ == "__main__":
    history = sys.argv[1]
    out = os.popen("phantomjs down.js \"%s\"" % history)
    content = out.read()
    dom = html.fromstring(content)
    print extract_link(dom, pub_templat)
    #for link in links:
    #    l = link.get("link")
    #    thum = link.get("thumb", "")
    #    article = down_article(l)
    #    dom = html.fromstring(article)
    #    article_content = extract(dom, newsTemplate)
    #    if not thum:
    #        thum = get_thumbnail(article_content)
    #        if not thum:
    #            thum = ""
    #    _id = int(time.time() * 1000)
    #    article_content.update({"_id": _id, "original_url": l, "image": thum})
    #    insert(article_content)
