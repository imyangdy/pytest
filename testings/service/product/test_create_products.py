# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
"""
# FileName： test_create_products.py
# Author : YuYanQing
# Desc: 创建实物商品
# Date： 2021/7/27 11:01
"""
import json
import pytest
from iutils.OkHttps import Httpx
from iutils.YamlUtils import YamlHandle
from testings.control.data import AWEN_TOKEN
from testings.control.init import Envision
from testings.control.path import NEW_SUCCED_PATH
from testings.control.url import CREATE_PRODUCT_URL
from testings.entity.Backend import setSampleProduct

# 标准写法
config = Envision.getYaml("boss_product_new.yaml")['config']
test_setup = Envision.getYaml("boss_product_new.yaml")['test_setup']


class TestCreateProduct():
    def test_new_succsed(self):
        """
        正常创建三个平台货号的商品
        :return:
        """
        data = setSampleProduct()
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=data,
                      esdata=[config, test_setup["new_succsed"]])
        YamlHandle.writeOjb(file_path=NEW_SUCCED_PATH, data=json.loads(data), method="w")

    def test_only_good_zlthird_sku_id(self):
        """
        创建单独的子龙货号商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(a8_third_sku_id="", gy_third_sku_id=""),
                      esdata=[config, test_setup["only_good_zlthird_sku_id"]])

    def test_only_good_a8third_sku_id(self):
        """
        创建单独的A8货号商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(zl_third_sku_id="", gy_third_sku_id=""),
                      esdata=[config, test_setup["only_good_a8third_sku_id"]])

    def test_only_good_gythird_sku_id(self):
        """
        创建单独的管易货号商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(zl_third_sku_id="", a8_third_sku_id=""),
                      esdata=[config, test_setup["only_good_gythird_sku_id"]])

    def test_lack_goods_name(self):
        """
        尝试创建缺少商品名称的商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(name=""),
                      esdata=[config, test_setup["lack_goods_name"]])

    def test_lack_goods_sort(self):
        """
        尝试创建缺少商品分类的商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(category_id="null"),
                      esdata=[config, test_setup["lack_goods_sort"]])

    def test_lack_good_third_sku_id(self):
        """
        尝试创建缺少商品货号的商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(zl_third_sku_id="", a8_third_sku_id="", gy_third_sku_id=""),
                      esdata=[config, test_setup["lack_good_third_sku_id"]])

    def test_lack_good_bar_code(self):
        """
        尝试创建缺少条形码的商品
        :return:
        """
        Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True,
                      hook_header=AWEN_TOKEN,
                      data=setSampleProduct(bar_code=""),
                      esdata=[config, test_setup["lack_good_bar_code"]])
