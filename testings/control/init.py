# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： init.py
# Author : YuYanQing
# Desc: 初始化运行环境
# Date： 2021/6/11 15:15
'''
import sys
sys.path.append('../')
from BaseSetting import Route
from iutils.LogUtils import Logger
from iutils.Loader import Loader
from testings.control.path import APPPROPERTIES_PATH

class Envision(object):
    def __init__(self):
        self.logger = Logger.writeLog()
        self.profiles =Loader.yamlFile(APPPROPERTIES_PATH)["profiles"]

    def getAuth(self):
        """
        获取认证信息
        :return:
        """
        return Loader.yamlFile(Route.joinPath("variables", "token.yaml"))

    def getHost(self,host):
        """
        获取自定义的域名
        :param host
        :return:
        """
        return str(Loader.yamlFile(Route.joinPath("properties", "dns_%s.yaml"%(str(self.profiles))))[host])

    def getAccunt(self,user):
        """
        获取用户组
        :param user:
        :return:
        """
        return Loader.yamlFile(Route.joinPath("variables", "user.yaml"))[user]

    def getAwenAdders(self, adders):
        """
        获取后台的地址
        :param adders 地址key
        :return:
        """
        return str(Loader.yamlFile(Route.joinPath("properties", "manager.yaml"))[adders])

    def getYaml(self,file_name):
        """
        读取Yaml_Case
        :param file_name:
        :return:
        """
        return Loader.yamlFile(Route.joinPath("test_yaml", file_name))

    def getJson(self,file_name):
        """
        读取Yaml_Case
        :param file_name:
        :return:
        """
        return Loader.jsonFile(Route.joinPath("test_json", file_name))

    def getCsv(self,file_name):
        """
        读取Yaml_Case
        :param file_name:
        :return:
        """
        return Loader.csvFile(Route.joinPath("test_csv", file_name))

    def getHeaders(self,method):
        """
        获取Json风格的头部
        :param method:
        :return:
        """
        text_plain = ['get', 'head', 'patch', 'options']
        json_method = ['post', 'put', 'delete']
        file_path = Route.joinPath("properties", "headers.yaml")
        headers = Loader.yamlFile(file_path)
        if method in text_plain:
            val = "get_headers"
        elif method in json_method:
            val = "json_headers"
        else:
            val = "from_headers"
        return headers[val]

Envision = Envision()

if __name__ == '__main__':
    print(Envision.getHost("uupa"))
    print(Envision.getBlockeAdders("add_shop_cart"))
    print(Envision.getAccunt("ordinary_account"))
    print(Envision.getAwenAdders("create_product"))

