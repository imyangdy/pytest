# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： path.py
# Author : YuYanQing
# Desc: PATH常量池
# Date： 2021/8/19 10:55
'''
import os
import sys
sys.path.append('../')
from iutils.Loader import Loader
from BaseSetting import Route
VARIABLES_PATH = Route.getPath("variables")
LOCALHOST_PATH = Route.getPath("localhost")
PROPERTIES_PATH = Route.getPath("properties")
IMG_PATH = Route.getPath("test_img")
AWEN_TOKEN_PATH = os.path.join(VARIABLES_PATH, "awn_token.yaml")
BLOCK_TOKEN_PATH = os.path.join(VARIABLES_PATH, "block_token.yaml")
UAER_INFO_PATH = os.path.join(LOCALHOST_PATH,"user_info.yaml")
MEDI_AITEM_PATH = os.path.join(LOCALHOST_PATH, "media_item.yaml")
CATEGORY_PATH = os.path.join(LOCALHOST_PATH, "category_id.yaml")
SECKIL_LIST_PATH = os.path.join(LOCALHOST_PATH, "seckill_list.yaml")
WHITEL_LIST_PATH = os.path.join(PROPERTIES_PATH, "whitelist.yaml")
CHANNEL_CATEGORY_PATH = os.path.join(LOCALHOST_PATH, "channel_category_id.yaml")
APPPROPERTIES_PATH = os.path.join(Route.getPath("workspaces"),"application.properties.yaml")
NEW_SUCCED_PATH = os.path.join(Route.getPath("variables"),"new_succsed.yaml")
PROFILES = Loader.yamlFile(APPPROPERTIES_PATH)["profiles"]
APPLICATION_PATH = os.path.join(Route.getPath("workspaces"),"application-{}.yaml".format(PROFILES))
DNS_PATH = os.path.join(Route.getPath("properties"),"dns_{}.yaml".format(PROFILES))
ADDRESS_PATH = os.path.join(Route.getPath("properties"),"address.yaml")
USER_VARS_PATH = os.path.join(Route.getPath("properties"),"user_vars.yaml")