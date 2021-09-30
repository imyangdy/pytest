# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_get_seckill_activitylist.py
# Author : YuYanQing
# Desc: 获取秒杀活动列表
# Date： 2021/8/23 15:09
'''
import pytest
from iutils.AllureUtils import setTag
from iutils.OkHttps import Httpx
from iutils.Processor import JsonPath
from iutils.YamlUtils import YamlHandle
from testings.control.data import AWEN_TOKEN
from testings.control.path import SECKIL_LIST_PATH
from testings.control.url import SECKILL_LIST_URL
from testings.entity.Seckill import setSeckillList


class TestSeckillProduct():
    def test_full_query(self):
        setTag({"feature": "秒杀活动", "story": "查询秒杀活动", "title": "无过滤全量查询"})
        data = setSeckillList(status=0, page_index=1, page_size=15, order_by=1)
        response = Httpx.sendApi(method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        YamlHandle.writeOjb(SECKIL_LIST_PATH, Httpx.getContent(response), "w")

    def test_filter_status_query(self):
        setTag({"feature": "秒杀活动", "story": "查询秒杀活动", "title": "仅过滤四个状态"})
        stage = {"1": "未开始", "2": "进行中", "3": "已结束", "4": "已终止"}
        for key, value in stage.items():
            data = setSeckillList(status=key, page_index=1, page_size=15, order_by=1)
            response = Httpx.sendApi(method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN, params=data)
            content = JsonPath.find(Httpx.getContent(response), "$.data..status")
            if content is not False:
                pytest.assume([int(key) == index == True for index in content])
            else:
                pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_filter_page_index_query(self):
        setTag({"feature": "秒杀活动", "story": "查询秒杀活动", "title": "仅过滤状态+分页"})
        stage = {"1": "未开始", "2": "进行中", "3": "已结束", "4": "已终止"}
        count = 1
        for key, value in stage.items():
            data = setSeckillList(status=key, page_index=count, page_size=10 + count, order_by=1)
            response = Httpx.sendApi(method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN, params=data)
            pytest.assume(Httpx.getStatusCode(response) == 200)
            count += 1

    def test_filter_orderby_asce_query(self):
        setTag({"feature": "秒杀活动", "story": "查询秒杀活动", "title": "倒序排列"})
        data = setSeckillList(status="1", page_index=1, page_size=15, order_by=2)
        response = Httpx.sendApi(method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_filter_orderby_desc_query(self):
        setTag({"feature": "秒杀活动", "story": "查询秒杀活动", "title": "升序排列"})
        data = setSeckillList(status="1", page_index=1, page_size=15, order_by=2)
        response = Httpx.sendApi(method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN, params=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)
