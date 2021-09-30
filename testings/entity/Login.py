# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Login.py
# Author : YuYanQing
# Desc: Model备注信息
# Date： 2021/8/9 9:24
'''
import json
import sys
sys.path.append('../')
from urllib import parse
from iutils.OkHttps import Httpx
from iutils.LogUtils import Logger
from iutils.YamlUtils import YamlHandle
from iutils.Processor import JsonPath, HtmlPath
from testings.control.data import ACCOUNT
from testings.control.init import Envision as Env
from testings.control.path import AWEN_TOKEN_PATH, UAER_INFO_PATH
from testings.control.url import CAS_LOGIN_URL, CONSOLE_LOGIN_URL, CONSOLE_INIT_URL, BOSS_LOGIN_URL


class Login():
    def __init__(self):
        self.logger = Logger.writeLog()

    def getTgc(self):
        """
        登录获取ticket
        :param execution jwt换来的验证
        :return:
        """
        group = Env.getAccunt(ACCOUNT)
        selector = Httpx.sendApi(method="get", url=CAS_LOGIN_URL).text
        execution = HtmlPath.find(selector, "//input[@name='execution']/@value", 0)
        headers = {"content-type": "application/x-www-form-urlencoded"}
        FormData = {
            "type": "passwd",
            "username": str(group["username"]),
            "password": str(group["password"]),
            "rememberMe": "true",
            "execution": execution,
            "_eventId": "submit",
            "geolocation": ""
        }
        response = Httpx.sendApi(method="post", url=CAS_LOGIN_URL, headers=headers, data=FormData)
        ticket = Httpx.getCookies(response.cookies.items(), "ticket")
        self.logger.info("获取ticket：%s" % (ticket["ticket"]))
        return ticket

    def getCookies(self, ticket):
        """
        通过css/login换取cookies
        :param ticket:
        :return:
        """
        cookies = Httpx.sendApi(method="get", url=CONSOLE_LOGIN_URL, data=ticket).cookies
        self.logger.info("获取cookies：%s" % (str(cookies)))
        return cookies

    def getJwt(self, awt):
        """
        通过Cookies获取jwt
        :param awt
        :return:
        """
        response = Httpx.sendApi(method="post", url=CONSOLE_INIT_URL, cookies=awt)
        # 写入userNo
        userNo = json.loads(response.text)["data"]["user"]["userInfo"]
        YamlHandle.writeOjb(UAER_INFO_PATH, userNo, "w")
        jwt = JsonPath.find(json.loads(response.content), "$.data.jwt")[0]
        self.logger.info("获取jwt：%s" % (jwt))
        return jwt,userNo

    def getToken(self, jwt, cookies):
        """
        获取Token
        :param jwt:
        :param cookies:
        :return:
        """
        hook_headers={"userNo" : jwt[1]["userNo"],"userRealName" : parse.quote(jwt[1]["userRealName"])}
        response = Httpx.sendApi(method="post", url=BOSS_LOGIN_URL, json={"ticket": jwt[0]}, cookies=cookies)
        token = "Bearer %s" % (JsonPath.find(json.loads(response.content), "$.token")[0])
        hook_headers.update({"Authorization": token})
        YamlHandle.writeOjb(AWEN_TOKEN_PATH,hook_headers, "w")
        self.logger.info("获取Token：%s" % (response.content))
        return token

    def goToBoss(self):
        """
        登录
        :return:
        """
        tgc = self.getTgc()
        cookies = self.getCookies(tgc)
        jwt = self.getJwt(cookies)
        author = self.getToken(jwt, cookies)
        return author

if __name__ == '__main__':
    Login().goToBoss()