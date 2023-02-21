import base64
import datetime
import hashlib
import requests
import json


class YunTongXin():

    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid  #账户ID
        self.accountToken = accountToken  #授权令牌
        self.appId = appId  #应用id
        self.templateId = templateId  #模板id

    def get_request_url(self, sig):
        # ' /2013-12-26/Accounts/{accountSid}/SMS/TemplateSMS?sig={SigParameter}'
        url = self.base_url + '/2013-12-26/Accounts/{}/SMS/TemplateSMS?sig={}'.format(self.accountSid, sig)
        return url

    def get_timestamp(self):
        # 生成时间戳
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sig(self, timestamp):
        s = self.accountSid+self.accountToken+timestamp
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    def get_request_header(self, timestamp):
        s = self.accountSid + ':' + timestamp
        auth = base64.b64encode(s.encode()).decode()
        return {
            'Accept':'application/json',
            'Content-Type':'application/json;charset=utf-8',
            'Authorization': auth
            }

    def get_request_body(self, phone, code):
        return {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            "datas": [code, "3"]  #验证码和过期时间
        }

    def request_api(self, url, header, body):
        res = requests.post(url, headers=header, data=body)
        return res.text


    def run(self, phone, code):
        # 获取时间戳
        timestamp = self.get_timestamp()
        # 生成签名
        sig = self.get_sig(timestamp)
        # 生成业务url
        url = self.get_request_url(sig)
        # print(url)
        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        data = self.request_api(url, header, json.dumps(body))
        return data


if __name__ == '__main__':
    config = {
        "accountSid": "8aaf070881ad8ad4018204adbd1d169f",
        "accountToken": "297e7389b60b414dacba0478d6fa547a",
        "appId": "8aaf070881ad8ad4018204adbdf616a6",
        "templateId":1
    }

    a = YunTongXin(**config)
    res = a.run("15804316881", "713918")
    print(res)
