#coding=utf-8
#!/usr/bin/python
import hashlib
import requests


class Config:
    appid = ""
    mch_id = ""
    api_key = ""
    UNIFIEDORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    ORDERQUERY_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
    CLOSEORDER_URL = "https://api.mch.weixin.qq.com/pay/closeorder"
    REFUND_URL = "https://api.mch.weixin.qq.com/secapi/pay/refund"
    REFUNDQUERY_URL = "https://api.mch.weixin.qq.com/pay/refundquery"
    DOWNLOADBILL_URL = "https://api.mch.weixin.qq.com/pay/downloadbill"

    def __init__(self, appid, mch_id, api_key):
        self.appid = appid
        self.mch_id = mch_id
        self.api_key = api_key

config = Config("113432432", "97fdksfljkal", "sdfkjlasuoiewfljlj")


class ParameterNotEnough(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.value = message

    def __str__(self):
        return repr(self.value)


class WxData(object):
    def __init__(self, config, data):
        self._type = data.get("trade_type")
        check = self._check(data)
        if check:
            raise ParameterNotEnough("%s is needed" % check)
        else:
            self.config = config
            self.data = data

    def _check(self, data):
        pass

    def ArrayToXml(self, data):
        result = ["<xml>"]
        for k, v in data.items():
            if v.isdigit():
                result.append("<{0}><{1}></{0}>".format(k, v))
            else:
                result.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        return "".join(result)

    def makeSign(self, data):
        self.data['appid'] = self.config.appid
        self.data['mch_id'] = self.config.mch_id
        sort_key = sorted(self.data)
        stringA = []
        for k in sort_key:
            stringA.append("%s=%s" % (k, str(self.data.get(k))))
        stringA = '&'.join(stringA)
        stringA += "&key=%s" % self.config.api_key
        sign = hashlib.md5(stringA).hexdigest()

        return sign


class UnifiedOrderData(WxData):
    def __init__(self, data):
        super(UnifiedOrderData, self).__init__(config, data)

    def _check(self, data):
        _type = self._type
        key_list = ['body', 'out_trade_no', 'trade_type', 'notify_url']
        if _type == "JSAPI":
            key_new = ['openid']
        elif _type == 'NATIVE':
            key_new = ['product_id']
        key_list.extend(key_new)
        for k in key_list:
            if k not in data:
                return k
        return None

    def getData(self):
        sign = self.makeSign(self.data)
        self.data['sign'] = sign

        return self.ArrayToXml(self.data)


class BaseService(object):
    apiURL = ""
    IServiceRequest = ""

    def __init__(self, url, request_service=None):
        self.apiURL = url
        self.IServiceRequest = request_service

    def sendPost(self, xmlData):
        ret = self.IServiceRequest.sendPost(self.apiURL, xmlData)


class request_service:
    def sendPost(self, url, data):
        r = requests.post(url, data)
        return r.content

if __name__ == "__main__":
    data = {'body': "test", 'out_trade_no': '20161010101010',
            'trade_type': "JSAPI", "notify_url": "http://www.baidu.com",
            "openid": "ljkfsdjaljfkl;"}
    u = UnifiedOrderData(data)
    s_data = u.getData()
    print s_data
    r = request_service()
    BS = BaseService(config.UNIFIEDORDER_URL, r)
    print BS.sendPost(s_data)
