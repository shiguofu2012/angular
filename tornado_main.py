#coding=utf-8
import tornado.ioloop
import tornado.web
from db.infodb import get_Articles


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

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
        self.set_default_headers()
        self.write({"articles": arts})


application = tornado.web.Application([
    (r"/", MainHandler),
    ])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
