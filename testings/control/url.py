# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： url.py
# Author : YuYanQing
# Desc: URL常量池
# Date： 2021/8/19 10:36
'''

import sys
sys.path.append('../')
from testings.control.init import Envision as Env
from iutils.OkHttps import Httpx

RVETDNS = Env.getHost("rvet") # 阿闻后台的Host地址
BLOCKETTEDNS = Env.getHost("blockette") # 阿闻小程序Host地址
UUPADNS = Env.getHost("uupa") # 获取Token的Host地址
AWENDNS = Env.getHost("awen") # BOSS登录的Host地址

CAS_LOGIN_URL = Httpx.urlJoint(UUPADNS,Env.getAwenAdders("cas_login"))
CONSOLE_LOGIN_URL = Httpx.urlJoint(AWENDNS,Env.getAwenAdders("console_login"))
CONSOLE_INIT_URL = Httpx.urlJoint(AWENDNS,Env.getAwenAdders("console_init"))
BOSS_LOGIN_URL = Httpx.urlJoint(RVETDNS,Env.getAwenAdders("boss_login"))
CREATE_PRODUCT_URL = Httpx.urlJoint(RVETDNS,Env.getAwenAdders("create_product"))
MEDIA_ITEM_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("media_item"))
PRODUCT_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("product_list"))
CATEGORY_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("category_list"))
CHANNEL_CATEGORY_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("channel_category_list"))
CHANNEL_PRODUCT_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("channel_product_list"))
STORE_INFO_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("store_info"))
PRODUCT_EDIT_QUERY_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("product_edit_query"))
GJ_PRODUCT_EDIT_QUERY_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("gj_product_edit_query"))
CHANNEL_PRODUCT_EDIT_QUERY_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("channel_product_edit_query"))
COPY_CHANNEL_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("copy_channel"))
CHANNEL_UP_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("channel_up"))
CHANNEL_STATUS_REFRESH_URL= Httpx.urlJoint(RVETDNS, Env.getAwenAdders("channel_status_refresh"))
PRODUCT_TAGS_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("product_tags"))
MED_IAITEM_UPLOAD_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("media_item_upload"))

# 运营中心-秒杀活动
SECKILL_ADD_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_add"))
SECKILL_DETAIL_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_detail"))
SECKILL_EDIT_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_edit"))
SECKILL_STOP_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_stop"))
SECKILL_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_list"))
SECKILL_PRODUCT_ADD_OR_EDIT_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_product_add_or_edit"))
SECKILL_PRODUCT_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_product_list"))
SECKILL_PRODUCT_SELECT_LIST_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_product_select_list"))
SECKILL_PRODUCT_DETAIL_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_product_detail"))
SECKILL_PRODUCT_DELETE_URL = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("seckill_product_delete"))
MALL_PRODUCT_STOCK = Httpx.urlJoint(RVETDNS, Env.getAwenAdders("mall_product_stock"))

