# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_stop_activity.py
# Author : YuYanQing
# Desc: 停止秒杀活动
# Date： 2021/8/23 11:20
'''
import pytest
from pytest_assume.plugin import assume
from iutils.AllureUtils import setTag
from iutils.DataKit import conversType
from iutils.OkHttps import Httpx
from testings.control.data import AWEN_TOKEN
from testings.control.url import SECKILL_STOP_URL
from testings.entity.Backend import getUser
from testings.entity.Seckill import setStopSeckillActivity, selectActivityInfo, selectActivity

USER_ID = getUser("id")
USER_NAME = getUser("name")


class TestSeckillProduct():
    def test_stop_no_exists(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止不存在的活动"})
        data = setStopSeckillActivity(21575837, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动不存在"})

    def test_stop_no_start_null_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止未开始的活动-无商品的"})
        try:
            activity_id = selectActivity(1)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 3
                assert int(activity_info["is_system_end"][0]) == 0

    def test_stop_no_start_have_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止未开始的活动-有商品的"})
        try:
            activity_id = selectActivity(1)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 3
                assert int(activity_info["is_system_end"][0]) == 0

    def test_stop_no_start_userid_is_null(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止未开始的活动-userID是空值"})
        activity_id = selectActivity(1)[0]["id"]
        data = setStopSeckillActivity(activity_id, None, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "UserId为必填字段"})

    def test_stop_no_start_userid_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止未开始的活动-userID是空字符"})
        activity_id = selectActivity(1)[0]["id"]
        data = setStopSeckillActivity(activity_id, "", USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "UserId为必填字段"})

    def test_stop_no_start_username_is_null(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止未开始的活动-userName是空值"})
        activity_id = selectActivity(1)[0]["id"]
        data = setStopSeckillActivity(activity_id, USER_ID, None)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "UserName为必填字段"})

    def test_stop_no_start_username_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止未开始的活动-userName是空字符"})
        activity_id = selectActivity(1)[0]["id"]
        data = setStopSeckillActivity(activity_id, USER_ID, "")
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "UserName为必填字段"})

    # 停止已经开始的活动
    def test_stop_is_underway_have_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止进行中的活动-有商品的"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 3
                assert int(activity_info["is_system_end"][0]) == 0

    def test_stop_is_underway_not_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止进行中的活动-无商品的"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 3
                assert int(activity_info["is_system_end"][0]) == 0

    def test_stop_is_underway_userid_is_null(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止进行中的活动-userID是空值"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, None, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "UserId为必填字段"})

    def test_stop_is_underway_userid_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止进行中的活动-userID是空字符"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, "", USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "UserId为必填字段"})

    def test_stop_is_underway_userno_is_null(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止进行中的活动-UserName是空值"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, None)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "UserName为必填字段"})

    def test_stop_is_underway_userno_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止进行中的活动-userName是空字符"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, "")
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "UserName为必填字段"})

    # 停止结束的活动
    def test_stop_end_not_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止自然结束的活动-无商品"})
        try:
            activity_id = selectActivity(3)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "活动状态已经是已结束"})

    def test_stop_end_have_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止自然结束的活动-有商品"})
        try:
            activity_id = selectActivity(3)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "活动状态已经是已结束"})

    def test_stop_terminated_not_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止手动终止的活动-无商品"})
        try:
            activity_id = selectActivity(4)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                pytest.assume(Httpx.getContent(response) == {"msg": "活动状态已经是已结束"})
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 3
                assert int(activity_info["is_system_end"][0]) == 0

    def test_stop_terminated_have_product(self):
        setTag({"feature": "秒杀活动", "story": "停止活动", "title": "停止手动终止的活动-有商品"})
        try:
            activity_id = selectActivity(4)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            data = setStopSeckillActivity(activity_id, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_STOP_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                pytest.assume(Httpx.getContent(response) == {"msg": "活动状态已经是已结束"})
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 3
                assert int(activity_info["is_system_end"][0]) == 0


if __name__ == '__main__':
    TestSeckillProduct().test_stop_terminated_not_product()
