# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_select_shop_detail.py
# Author : YuYanQing
# Desc: Model备注信息
# Date： 2021/9/10 19:03
'''
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("product_api_shop_detail.yaml")['config']
test_setup = Envision.getYaml("product_api_shop_detail.yaml")['test_setup']

class TestDetail():
    def test_select_shop_detail(self):
        Httpx.sendApi(auto=True, esdata=[config, test_setup["view_store_details"]])

