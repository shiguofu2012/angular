#!/usr/bin/python
from lxml import html
from process_article import get_text, get_pic
import requests
import uuid

IMG_REP_STR = "<div>&lte;picturestart--%s--pictureend&gte;</div>"
templat = {
        "block": "//div[@class=\"msg_list_bd\"]",
        "subblock": ".//div[@class=\"sub_msg_list\"]",
        "time": ".//p[@class=\"msg_date\"]",
        "title": ".//h4[@class=\"msg_title\"]/text()",
        "link": ".//a[@class=\"sub_msg_item redirect\"]/@hrefs",
        "picture": ".//span[@class=\"thumb\"]/img/@data-src"
        }


newsTemplate = {
        "title": "//h2/text()",
        "content": "//div[@id=\"img-content\"]",
        "pubDate": "",
        "remove": ".//section[@label=\"powered by 135editor.com\"]/p[position() > last() - 18]&.//div[@class=\"rich_media_tool\"]"
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


def down_article(link):
    r = requests.get(link)
    if r.ok:
        return r.content
    else:
        return None


def remove_tag(dom, xpath_str):
    xpath_str = "|".join(xpath_str.split("&"))
    tag_remove = dom.xpath(xpath_str)
    for tag in tag_remove:
        parent_node = tag.getparent()
        parent_node.remove(tag)


def extract_item(dom, item, template, multi=False):
    if item not in template and not template.get(item):
        return ""
    item_value = dom.xpath(template[item])
    if multi:
        return item_value
    return item_value[0]


def extract(dom, template):
    article = {}
    tag_remove = template.get("remove", "")
    article['title'] = extract_item(dom, 'title', template)
    content = extract_item(dom, "content", template)
    text = ""
    remove_tag(content, tag_remove)
    pics = get_pic(content)
    for p in pics:
        node = p.get("node")
        parent_node = node.getparent()
        parent_node.replace(node, html.fromstring(IMG_REP_STR % p.get("id")))
    text += get_text(content)
    article["content"] = text
    return article


if __name__ == "__main__":
    f = open("wuhan.html")
    content = f.read()
    f.close()
    dom = html.fromstring(content)
    #r = extract_link(dom, templat)
    #print r
    links = extract_link(dom, templat)
    link = links[1].get("link")
    article = down_article(link)
    dom = html.fromstring(article)
    print link
    result = extract(dom, newsTemplate)
    print result.get("content")
    #content = dom.xpath("//div[@id=\"img-content\"]")[0]
    #remove_tag = content.xpath(
    #        ".//p[position() > 49] | .//div[@class=\"rich_media_tool\"]")
    #remove_tag = content.xpath(".//div[@class=\"rich_media_tool\"]")
    #remove_tag(content,
    #        ".//section[@label=\"powered by 135editor.com\"]/p[position() > last() - 18]&.//div[@class=\"rich_media_tool\"]")
    #pics = get_pic(content)
    #for pic in pics:
    #    node = pic.pop("node")
    #    parent_node = node.getparent()
    #    parent_node.replace(node, html.fromstring(("<div>&lte;picturestart--%s--pictureend&gte;</div>" % pic.get("id"))))
    #print get_text(content)
    #for i in content:
    #    if i.tag == 'script':
    #        continue
    #    print i.tag
