#coding=utf-8
import tornado.ioloop
import tornado.web
import re
from db.infodb import get_Articles, get_OneArticle, get_ImageByCond

PATTERN_IMG = re.compile("&ltpicturestart--(.*?)--pictureend&gt")
PATTERN_STR = "&ltpicturestart--%s--pictureend&gt"


def set_default_headers(self):
    self.set_header('Access-Control-Allow-Origin', '*')
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    self.set_header('Access-Control-Max-Age', 1000)
    self.set_header('Access-Control-Allow-Headers', '*')
    self.set_header('Content-type', 'application/json')


def ship_article(art):
    title = art.get("title", "")
    content = art.get("content", "")
    pubDate = art.get("pubDate")
    imgs = PATTERN_IMG.findall(content)
    images = get_ImageByCond({"id": {"$in": imgs}})
    image_dict = {}
    for image in images:
        _id = image.get("id")
        image_dict[_id] = image
    for img in imgs:
        image = image_dict.get(img)
        if image:
            url = image.get("url")
        else:
            url = ""
        repStr = "<img src=" + url + ">"
        content = content.replace(PATTERN_STR % img, repStr)
    con_list = content.split("\n")
    content = ""
    for con in con_list:
        if not con or content == ' ':
            continue
        content += "<p>" + con + "</p>"
    return {"title": title, "content": content, "time": pubDate}


def ship_article_list(art):
    title = art.get("title", "")
    image = art.get("image", "")
    pubDate = art.get("pubDate")
    _id = art.get("_id")
    url = art.get("url")
    return {"title": title, "id": _id, "image": image, "pubDate": pubDate}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        page = self.get_argument("page", 1)
        count = self.get_argument("count", 10)
        try:
            page = int(page)
            count = int(count)
        except Exception as e:
            page = 1
            count = 10
        arts = get_Articles((page - 1) * count, count)
        result = []
        for art in arts:
            info = ship_article_list(art)
            result.append(info)
        set_default_headers(self)
        self.write({"articles": result})


class TestHandler(tornado.web.RequestHandler):
    def get(self, cid):
        try:
            cid = int(cid)
        except Exception as e:
            self.write({"err": -1, "errmsg": e})
        set_default_headers(self)
        art = get_OneArticle(cid)
        art = ship_article(art)
        self.write({"article": art})


application = tornado.web.Application([
    (r"/article/list", MainHandler),
    (r"/article/(.*?)", TestHandler),
    ])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
