# -*-coding:utf-8-*-
import json
import os

import OpenSSL
import requests

from auto_ui import settings


class Http:
    def __init__(self, model):
        self.model = model

    def __request(self, **kwargs):
        try:
            if self.model.lower() == "get":
                response = requests.request("get", kwargs["url"], params=kwargs["params"], headers=kwargs["headers"],
                                            cookies=kwargs["cookies"])
            # post的参数名要为data
            elif self.model.lower() == "postbody":
                # 转换成字符串传入
                # params = json.dumps(kwargs["params"], ensure_ascii=False)
                # params = json.loads(kwargs["params"])
                response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                            cookies=kwargs["cookies"])
            elif self.model.lower() == "postform":
                response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                            cookies=kwargs["cookies"])
            elif self.model.lower() == "postfile":
                response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                            files=kwargs["files"], cookies=kwargs["cookies"])

            return response
        except BaseException as e:
            return ("error{0}".format(str(e)))

    def __requests(self, **kwargs):
            try:
                if self.model.lower() == "get":
                    response = requests.request("get", kwargs["url"], params=kwargs["params"],headers=kwargs["headers"],
                                                cookies=kwargs["cookies"])
                # post的参数名要为data
                elif self.model.lower() == "postbody":
                    # 转换成字符串传入
                    # params = json.dumps(kwargs["params"], ensure_ascii=False)
                    # params = json.loads(kwargs["params"])
                    response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                                cookies=kwargs["cookies"])
                elif self.model.lower() == "postform":
                    response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                                cookies=kwargs["cookies"])
                elif self.model.lower() == "postfile":
                    response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                                files=kwargs["files"], cookies=kwargs["cookies"])

                return response
            except BaseException as e:
                return ("error{0}".format(str(e)))

    # 文本转换成json字符串
    def __changeJson(self, response):
        responseJson = json.loads(response.text)
        return responseJson

    def __call__(self, fuc):
        def wrapper(*args, **kwargs):
            fuc(*args, **kwargs)
            if 'https' in kwargs['url']:
                response = self.__requests(**kwargs)
            else:
                response = self.__request(**kwargs)
            # responseJson = self.__changeJson(response)
            return response

        return wrapper


    def p12_to_pem(self):
        pem_name = os.path.join(settings.BASE_DIR,'conf','pem_name.pem')
        f_pem = open(pem_name, 'wb')
        p12file = os.path.join(settings.BASE_DIR,'conf','pem_name.p12')
        p12 = OpenSSL.crypto.load_pkcs12(open(p12file, 'rb').read(), '123456')
        f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
        f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
        ca = p12.get_ca_certificates()
        if ca is not None:
            for cert in ca:
                f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
        f_pem.close()
        return pem_name

@Http(model="GET")
def get(url, params, headers, cookies=''):
    pass


@Http(model="POSTFORM")
def postform(url, params, headers, cookies):
    pass


@Http(model="POSTBODY")
def postbody(url, params, headers, cookies):
    pass


@Http(model="POSTFILE")
def postfile(url, params, headers, files, cookies):
    pass
