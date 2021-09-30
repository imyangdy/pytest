# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： data.py
# Author : YuYanQing
# Desc:  变量池
# Date： 2021/8/19 9:46
'''
import random
import sys
sys.path.append('../')
from iutils.Loader import Loader
from testings.control.path import AWEN_TOKEN_PATH,BLOCK_TOKEN_PATH,UAER_INFO_PATH,CATEGORY_PATH,APPPROPERTIES_PATH,NEW_SUCCED_PATH,\
    WHITEL_LIST_PATH,APPLICATION_PATH

ACCOUNT = Loader.yamlFile(APPPROPERTIES_PATH)["account"]
APPLICATION = Loader.yamlFile(APPLICATION_PATH)
DB_CONFIG = APPLICATION["database"]
AWEN_TOKEN = Loader.yamlFile(AWEN_TOKEN_PATH)
BLOCK_TOKEN = Loader.yamlFile(BLOCK_TOKEN_PATH)
BLOCKET_TETOKEN = Loader.yamlFile(AWEN_TOKEN_PATH)
USER_INFO = Loader.yamlFile(UAER_INFO_PATH)
CATEGORYID = Loader.yamlFile(CATEGORY_PATH)
NEWSUCCED = Loader.yamlFile(NEW_SUCCED_PATH)
ACTIVITY_WHITEL_LIST = Loader.yamlFile(WHITEL_LIST_PATH)["activity"]
AUTO = "PY自动化"