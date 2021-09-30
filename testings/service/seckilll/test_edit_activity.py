# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_edit_activity.py
# Author : YuYanQing
# Desc: 修改秒杀活动
# Date： 2021/8/23 11:20
'''

import pytest
from pytest_assume.plugin import assume
from iutils.AllureUtils import setTag
from iutils.DataKit import conversType
from iutils.DateUtils import Moment
from iutils.OkHttps import Httpx
from iutils.RandUtils import RandValue
from testings.control.data import AWEN_TOKEN, AUTO, ACTIVITY_WHITEL_LIST
from testings.control.sql import connActivity
from testings.control.url import SECKILL_EDIT_URL
from testings.entity.Backend import getUser
from testings.entity.Seckill import setEditSeckillActivity, getSeckillActivityTime, selectActivityInfo, grepActivity

USER_ID = getUser("id")
USER_NAME = getUser("name")


class TestSeckillProduct():
    def test_edit_not_exits(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改不存在的活动"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("10001,200001")
        is_shipping_free = 0
        data = setEditSeckillActivity(505550, title, begin_time, end_time, seckill_order_limit, is_shipping_free,
                                      USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动不存在"})

    def test_edit_id_is_null(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "活动id值是None"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("10001,200001")
        is_shipping_free = 0
        data = setEditSeckillActivity(None, title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                      USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动不存在"})

    def test_edit_id_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "活动id值是空字符"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("10001,200001")
        is_shipping_free = 0
        data = setEditSeckillActivity("", title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                      USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "请求参数格式有误"})

    def test_edit_id_is_not_exits(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "活动id值不传"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("10001,200001")
        is_shipping_free = 1
        data = {"title": title, "begin_time": begin_time, "end_time": end_time,
                "seckill_order_limit": seckill_order_limit,
                "is_shipping_free": is_shipping_free, "user_id": USER_ID, "user_name": USER_NAME}
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动不存在"})

    def test_edit_no_start_not_product(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改未开始的活动-无商品"})
        title = AUTO + str(RandValue.getStr(18)).title()
        try:
            activity_id = grepActivity(method="not in",status=1)["id"][0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
            end_time = Moment.computeDate(minutes=7, custom=begin_time)
            seckill_order_limit = RandValue.getInt("10001,200001")
            activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
            old_is_shipping_free = int(activity_info["is_shipping_free"][0])
            is_shipping_free =1 if old_is_shipping_free == 0 else 0
            data = setEditSeckillActivity(activity_id, title, begin_time, end_time, seckill_order_limit,
                                          is_shipping_free, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 1
                assert activity_info["is_system_end"][0] == 0
                assert str(activity_info["begin_time"][0]) == begin_time
                assert str(activity_info["end_time"][0]) == end_time
                assert int(activity_info["is_shipping_free"][0]) == int(is_shipping_free)
                assert int(activity_info["seckill_order_limit"][0]) == int(seckill_order_limit)

    def test_edit_no_start_have_product(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改未开始的活动-有商品"})
        title = AUTO + str(RandValue.getStr(18)).title()
        try:
            activity_id = grepActivity(method="in",status=1)["id"][0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
            end_time = Moment.computeDate(minutes=7, custom=begin_time)
            seckill_order_limit = RandValue.getInt("10001,200001")
            activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
            old_is_shipping_free = int(activity_info["is_shipping_free"][0])
            is_shipping_free = 1 if old_is_shipping_free == 0 else 0
            data = setEditSeckillActivity(activity_id, title, begin_time, end_time, seckill_order_limit,
                                          is_shipping_free, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 1
                assert activity_info["is_system_end"][0] == 0
                assert str(activity_info["begin_time"][0]) == begin_time
                assert str(activity_info["end_time"][0]) == end_time
                assert int(activity_info["is_shipping_free"][0]) == int(is_shipping_free)
                assert int(activity_info["seckill_order_limit"][0]) == int(seckill_order_limit)

    def test_edit_underway_have_product(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改进行中的活动-有商品"})
        title = AUTO + str(RandValue.getStr(18)).title()
        try:
            activity_id = grepActivity(method="in",status=2)["id"][0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
            end_time = Moment.computeDate(minutes=7, custom=begin_time)
            activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
            old_is_shipping_free = int(activity_info["is_shipping_free"][0])
            old_seckill_order_limit = int(activity_info["seckill_order_limit"][0])
            is_shipping_free = 1 if old_is_shipping_free == 0 else 0
            seckill_order_limit = 1 if int(old_seckill_order_limit-1)<0 else int(old_seckill_order_limit-1)
            data = setEditSeckillActivity(activity_id, title, begin_time, end_time, seckill_order_limit,
                                          is_shipping_free, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 2
                assert int(activity_info["is_system_end"][0]) == 0
                assert str(activity_info["begin_time"][0]) != begin_time
                assert str(activity_info["end_time"][0]) != end_time
                assert str(activity_info["is_shipping_free"][0]) != is_shipping_free
                assert str(activity_info["seckill_order_limit"][0]) != seckill_order_limit

    def test_edit_underway_not_have_product(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改进行中的活动-无商品"})
        title = AUTO + str(RandValue.getStr(18)).title()
        try:
            activity_id = grepActivity(method="not in",status=2)["id"][0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
            end_time = Moment.computeDate(minutes=7, custom=begin_time)
            activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
            old_is_shipping_free = int(activity_info["is_shipping_free"][0])
            old_seckill_order_limit = int(activity_info["seckill_order_limit"][0])
            is_shipping_free = 1 if old_is_shipping_free == 0 else 0
            seckill_order_limit = int(old_seckill_order_limit+1) if int(old_seckill_order_limit - 1) < 0 else int(old_seckill_order_limit - 1)
            data = setEditSeckillActivity(activity_id, title, begin_time, end_time, seckill_order_limit,
                                          is_shipping_free, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
            with assume:
                assert Httpx.getStatusCode(response) == 200
                activity_info = selectActivityInfo(keyword="where id = {}".format(activity_id)).to_dict()
                assert activity_info["id"][0] == activity_id
                assert int(activity_info["channel_id"][0]) == 5
                assert int(activity_info["types"][0]) == 11
                assert int(activity_info["status"][0]) == 2
                assert int(activity_info["is_system_end"][0]) == 0
                assert str(activity_info["begin_time"][0]) != begin_time
                assert str(activity_info["end_time"][0]) != end_time
                assert str(activity_info["is_shipping_free"][0]) == is_shipping_free
                assert str(activity_info["seckill_order_limit"][0]) != str(seckill_order_limit)

    def test_edit_end(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改自然结束的活动"})
        title = AUTO + str(RandValue.getStr(18)).title()
        activity_id = connActivity.callSql(
            "select promotion.id from promotion where promotion.id not in (select promotion_product.promotion_id from promotion_product) "
            "and promotion.status = 3 and promotion.id in {} and promotion.is_system_end =0 ".format(tuple(ACTIVITY_WHITEL_LIST))).to_dict()["id"][0]
        if activity_id == {}:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
            end_time = Moment.computeDate(minutes=7, custom=begin_time)
            seckill_order_limit = RandValue.getInt("10001,200001")
            is_shipping_free = 0
            data = setEditSeckillActivity(activity_id, title, begin_time, end_time, seckill_order_limit,
                                          is_shipping_free, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "已结束的活动不能编辑"})

    def test_edit_terminated(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "修改手动终止的活动"})
        title = AUTO + str(RandValue.getStr(18)).title()
        activity_id = connActivity.callSql("select promotion.id from promotion where promotion.id "
                                           "not in (select promotion_product.promotion_id from promotion_product) "
                                           "and promotion.status = 3 and promotion.id in {} and promotion.is_system_end =1 ".format(tuple(ACTIVITY_WHITEL_LIST))).to_dict()["id"][0]
        if activity_id =={}:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
            end_time = Moment.computeDate(minutes=7, custom=begin_time)
            seckill_order_limit = RandValue.getInt("10001,200001")
            is_shipping_free = 0
            data = setEditSeckillActivity(activity_id, title, begin_time, end_time, seckill_order_limit,
                                          is_shipping_free, USER_ID, USER_NAME)
            conversType(data, ["user_id"])
            response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
            pytest.assume(Httpx.getContent(response) == {"msg": "已结束的活动不能编辑"})

    def test_edit_all_null(self):
        setTag({"feature": "秒杀活动", "story": "修改活动", "title": "所有字段值均为空"})
        response = Httpx.sendApi(method="post", url=SECKILL_EDIT_URL, hook_header=AWEN_TOKEN,
                                 json=setEditSeckillActivity())
        pytest.assume(Httpx.getContent(response) == {"msg": "活动名称为必填字段"})


if __name__ == '__main__':
    TestSeckillProduct().test_edit_no_start_have_product()
