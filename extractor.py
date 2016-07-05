#!/usr/bin/python
from lxml import html

templat = {
        "block": "//div[@class=\"msg_list_bd\"]",
        "subblock": ".//div[@class=\"sub_msg_list\"]",
        "time": ".//p[@class=\"msg_date\"]",
        "title": ".//h4[@class=\"msg_title\"]/text()",
        "link": ".//a[@class=\"sub_msg_item redirect\"]/@hrefs",
        "picture": ".//span[@class=\"thumb\"]/img/@data-src"
        }


def extract_link(dom, template):
    result = []
    blocks = dom.xpath(templat["block"])
    print blocks
    for block in blocks:
        t = block.xpath(templat['time'])
        articles = block.xpath(templat['subblock'])
        for a in articles:
            title = a.xpath(templat['title'])
            if title and isinstance(title, list):
                title = title[0]
            link = a.xpath(templat['link'])
            if link and isinstance(link, list):
                link = link[0]
            pic = a.xpath(templat['picture'])
            if pic and isinstance(pic, list):
                pic = pic[0]
            if not pic:
                print title
            tmp = {}
            tmp['title'] = title
            tmp['link'] = link
            tmp['thumb'] = pic
            result.append(tmp)
    print len(result)
    for i in result:
        title = i.get("title", "")
        link = i.get("link", "")
        pic = i.get("thumb", '')
        #print pic
    return result


if __name__ == "__main__":
    f = open("wuhan.html")
    content = f.read()
    f.close()
    dom = html.fromstring(content)
    r = extract_link(dom, templat)
    print r
