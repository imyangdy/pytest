# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： BasePath.py
# Author : YuYanQing
# Desc: 声明目录结构
# Date： 2020/7/15 16:15
'''
import os
import time

class Route(object):
    def __init__(self):
        """
        统一配置yaml文件及报告产生的路径
        """
        self.workspaces = os.path.abspath(os.path.dirname(__file__))
        self.path = {"output": "output",
                     "config": "config",
                     "allure_result": "allure_result",
                     "allure_report": "allure_report",
                     "test_path": r"testings",
                     "test_img": r"testings/dao/test_img",
                     "test_csv": r"testings/dao/test_csv",
                     "test_json": r"testings/dao/test_json",
                     "test_yaml": r"testings/dao/test_yaml",
                     "properties" : r"testings/config/properties",
                     "variables" : r"testings/config/variables",
                     "localhost" : r"testings/config/localhost",
                     }

    def getPath(self,keyword):
        """
        获取路径
        :param keyword:
        :return:
        """
        if keyword == "workspaces":
            return self.workspaces
        else:
            return os.path.join(self.workspaces, self.path[keyword])

    def joinPath(self,file_path,file_name):
        """
        拼接路径
        :param file_path 文件路径
        :param file_name 文件名
        :return:
        """
        return os.path.join(Route.getPath(file_path), file_name)

Route = Route()

if __name__ == '__main__':
    print(Route.getPath("workspaces"))
    print(Route.getPath("variables"))
    print(Route.joinPath("test_yaml", "boss_product_new.yaml"))
