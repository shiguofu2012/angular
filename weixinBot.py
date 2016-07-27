#!/usr/bin/python
import time
import json
import qrcode
import sys
import re
import urllib
import urllib2
import xml.dom.minidom


UUIDURL = "https://login.weixin.qq.com/jslogin"
QRCODEURL = "https://login.weixin.qq.com/l/"
SCANURL = "https://login.weixin.qq.com" +\
        "/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s"


class wxBot(object):
    def __init__(self, lang='zh_CN'):
        self.uuid = ""
        self.uin = ''
        self.sid = ''
        self.skey = ''
        self.uri = ''
        self.base_uri = ''
        self.pass_ticket = ''
        self.lang = lang
        self.appid = 'wx782c26e4c19acffb'

    def getUUID(self):
        params = {
                'appid': self.appid,
                'fun': 'new',
                'lang': self.lang,
                '_': int(time.time())
                }
        data = self._post(UUIDURL, params, False)
        print data
        rege = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(rege, data)
        if pm:
            code = pm.group(1)
            self.uuid = pm.group(2)
            return code == '200'
        return False

    def genQR(self):
        if sys.platform.startswith('linux'):
            self._str2qr(QRCODEURL + self.uuid)

    def _str2qr(self, s):
        qr = qrcode.QRCode()
        qr.border = 1
        qr.add_data(s)
        mat = qr.get_matrix()
        self.printQR(mat)

    def printQR(self, matrix):
        BLACK = '\033[40m  \033[0m'
        WHITE = '\033[47m  \033[0m'
        for i in matrix:
            print ''.join([BLACK if j else WHITE for j in i])

    def waitScan(self, tip=1):
        time.sleep(tip)
        url = SCANURL % (tip, self.uuid, int(time.time()))
        data = self._get(url)
        regex_status = r'window.code=(\d+);'
        regex_reuri = r'window.redirect_uri="(\S+?)"'
        pm = re.search(regex_status, data)
        code = pm.group(1)
        if code == '201':
            print 'wait scan'
            return True
        elif code == '200':
            print 'scan ok'
            pm = re.search(regex_reuri, data)
            uri = pm.group(1)
            self.uri = uri + "&fun=new"
            self.base_uri = uri[:uri.rfind('/')]
            return True
        else:
            print 'login error'
            return False

    def getData(self):
        content = self._get(self.uri)
        doc = xml.dom.minidom.parseString(content)
        root = doc.documentElement
        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.skey = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.sid = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.uin = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.pass_ticket = node.childNodes[0].data
        print self.skey
        print self.sid
        print self.uin
        print self.pass_ticket

    def _post(self, url, params, jsonfmt):
        if jsonfmt:
            req = urllib2.Request(url=url, data=json.dumps(params))
            req.add_header("contentType", "application/json;charset=UTF-8")
        else:
            req = urllib2.Request(url=url, data=urllib.urlencode(params))
        resp = urllib2.urlopen(req)
        data = resp.read()
        if jsonfmt:
            return json.loads(data)
        return data

    def _get(self, url):
        req = urllib2.Request(url=url)
        resp = urllib2.urlopen(req)
        data = resp.read()
        return data

    def login(self):
        if(self.getUUID()):
            print 'gen qrcode ...'
            self.genQR()
            while 1:
                print 'wait...'
                r = self.waitScan()
                if r and not self.uri:
                    continue
                else:
                    break
            self.getData()
        else:
            print "uuid error"


if __name__ == "__main__":
    w = wxBot()
    w.login()
