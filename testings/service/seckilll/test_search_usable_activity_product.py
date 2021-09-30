# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_search_seckill_product.py
# Author : YuYanQing
# Desc: 搜索可用的活动的商品
# Date： 2021/8/23 18:30
'''
import random

import pytest
from iutils.AllureUtils import setTag
from iutils.OkHttps import Httpx
from testings.control.data import ACTIVITY_WHITEL_LIST
from testings.control.url import SECKILL_PRODUCT_SELECT_LIST_URL
from testings.entity.Seckill import setSeckillProductSearch, AWEN_TOKEN

PROMOTION_ID = int(random.sample(ACTIVITY_WHITEL_LIST, 1)[0])

class TestSeckillProduct():
    def test_seek_all_product(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "无过滤条件"})
        data = setSeckillProductSearch(page_index=1, page_size=15, promotion_id=PROMOTION_ID, product_name="",
                                       sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN,
                                 params=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_seek_product_pageindex_is_null(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "PageIndex值是NULL"})
        data = setSeckillProductSearch(page_index=None, page_size=15, promotion_id=PROMOTION_ID, product_name="",
                                       sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    def test_seek_product_pageindex_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "PageIndex值是空字符"})
        data = setSeckillProductSearch(page_index="", page_size=15, promotion_id=PROMOTION_ID, product_name="",
                                       sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    def test_seek_product_pagesize_is_null(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "PageSize值是NULL"})
        data = setSeckillProductSearch(page_index=15, page_size=None, promotion_id="15", product_name="", sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    def test_seek_product_pagesize_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "PageSize值是空字符"})
        data = setSeckillProductSearch(page_index=1, page_size="", promotion_id=PROMOTION_ID, product_name="",
                                       sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    def test_seek_product_promotion_id_is_null(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "PromotionId值是NULL"})
        data = setSeckillProductSearch(page_index=1, page_size=15, promotion_id=None, product_name="", sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    def test_seek_product_promotion_id_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "PromotionId值是空字符"})
        data = setSeckillProductSearch(page_index="", page_size=15, promotion_id="", product_name="", sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    def test_seek_product_other_is_null(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "非必填项值是NULL"})
        data = setSeckillProductSearch(page_index=1, page_size=15, promotion_id=PROMOTION_ID, product_name="",
                                       sku_id="",
                                       spu_id="")
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_seek_product_other_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "非必填项值是空字符"})
        data = setSeckillProductSearch(page_index=1, page_size=15, promotion_id=PROMOTION_ID, product_name=None,
                                       sku_id=None,
                                       spu_id=None)
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_seek_product_activity_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "搜索活动下的商品", "title": "活动不存在"})
        data = setSeckillProductSearch(page_index=1, page_size=15, promotion_id=2147483647, product_name=None,
                                       sku_id=None,
                                       spu_id=None)
        response = Httpx.sendApi(method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动不存在", "total": 0, "data": []})
