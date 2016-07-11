#coding=utf-8
import tornado.ioloop
import tornado.web
from db.infodb import get_Articles


def set_default_headers(self):
    self.set_header('Access-Control-Allow-Origin', '*')
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    self.set_header('Access-Control-Max-Age', 1000)
    self.set_header('Access-Control-Allow-Headers', '*')
    self.set_header('Content-type', 'application/json')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        arts = get_Articles(0, 10)
        for art in arts:
            content = art.get("content")
            content_list = content.split("\n")
            content = ""
            print len(content_list)
            for c in content_list:
                content += "<p>%s</p>" % c
            art['content'] = content
        set_default_headers(self)
        self.write({"articles": arts})


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        set_default_headers(self)
        f = open("test.html")
        content = f.read()
        f.close()
        return content


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test.html", TestHandler),
    ])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
