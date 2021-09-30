# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_add_activity.py
# Author : YuYanQing
# Desc: 添加秒杀活动
# Date： 2021/8/23 11:20
'''
import sys
import pytest
from iutils.AllureUtils import setTag
from iutils.DataKit import conversType
from iutils.DateUtils import Moment
from iutils.OkHttps import Httpx
from iutils.RandUtils import RandValue
from testings.control.data import AUTO, AWEN_TOKEN
from testings.control.sql import connActivity
from testings.control.url import SECKILL_ADD_URL
from testings.entity.Backend import getUser
from testings.entity.Seckill import setAddSeckillActivity, getSeckillActivityTime

USER_ID = getUser("id")
USER_NAME = getUser("name")


class TestSeckillProduct():
    # 正常创建活动
    def test_add_success(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "所有字段均传有效值"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    # 活动标题字段检查
    def test_add_title_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动标题是None"})
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(None, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动名称为必填字段"})

    def test_add_title_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动标题是空字符"})
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity("", begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动名称为必填字段"})

    def test_add_title_gr_upper(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动标题>25字符"})
        title = AUTO + str(RandValue.getStr(21)).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动名称最多可输入25个字符"})

    # 活动开始时间字段检查
    def test_add_past_time(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间是过去的时间"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = Moment.computeDate(days=-1, custom=Moment.getTime("%Y-%m-%d %H:%M:%S"))
        end_time = Moment.computeDate(minutes=7, custom=str(begin_time))
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动开始时间不能为过去的时间"})

    def test_add_begintime_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间值是NULL"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, None, end_time, seckill_order_limit, is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动开始时间为必填字段"})

    def test_add_begintime_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间是空字符"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        end_time = getSeckillActivityTime()
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, "", end_time, seckill_order_limit, is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动开始时间为必填字段"})

    def test_add_begintime_is_illegal(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间不合法"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        end_time = Moment.computeDate(minutes=7, custom=getSeckillActivityTime())
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, "错误时间", end_time, seckill_order_limit, is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动开始时间格式错误"})

    def test_add_begintime_is_illegal(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间>当前时间>结束时间"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=-60, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动结束时间必须晚于开始时间"})

    def test_add_time_equality(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间>（当前时间=结束时间）"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, begin_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动结束时间不能等于活动开始时间"})

    def test_add_time_begin_overlap(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间=当前进行中活动begin_time~end_time"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        activity_time = connActivity.callSql(
            "select title,begin_time,end_time from promotion where status =2 order by end_time desc ").to_dict()
        begin_time = activity_time["begin_time"][0].strftime('%Y-%m-%d %H:%M:%S')
        end_time = activity_time["end_time"][0].strftime('%Y-%m-%d %H:%M:%S')
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动开始时间不能为过去的时间"})

    def test_add_time_on_start_overlap(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动开始时间=未开始活动begin_time~end_time重叠"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        activity_time = connActivity.callSql(
            "select title,begin_time,end_time from promotion where status =1 order by end_time desc ").to_dict()
        orvelap_title = activity_time["title"][0]
        begin_time = activity_time["begin_time"][0].strftime('%Y-%m-%d %H:%M:%S')
        end_time = activity_time["end_time"][0].strftime('%Y-%m-%d %H:%M:%S')
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动时间与%s活动时间有重叠" % (orvelap_title)})

    # 活动结束时间字段检查
    def test_add_endtime_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动结束时间值是NULL"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, None, seckill_order_limit, is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动结束时间为必填字段"})

    def test_add_endtime_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动结束时间是空字符"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, "", seckill_order_limit, is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动结束时间为必填字段"})

    def test_add_endtime_is_illegal(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动结束时间不合法"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, "错误时间", seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "活动结束时间格式错误"})

    # 限购字段效验
    def test_add_purchas_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动限购数是None"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, None, is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_add_purchas_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动限购数是空字符"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, "", is_shipping_free, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "请求参数格式有误"})

    def test_add_purchas_is_gr_lower(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动限购数超出最小边界值"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = -1
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "购买上限最小只能为0"})

    def test_add_purchas_is_gr_upper(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动限购数超出最大边界值"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = sys.maxsize
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    # 免邮字段效验
    def test_add_free_shipping_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动免邮是None"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, None, USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_add_free_shipping_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动免邮是空字符"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, "", USER_ID, USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "请求参数格式有误"})

    def test_add_free_shipping_is_gr_astrict(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "活动免邮值不是0或1"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = sys.maxsize
        count = 0
        for index in range(RandValue.getInt("1,%s" % (is_shipping_free)), is_shipping_free):
            if count < 3:
                data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free,
                                             USER_ID, USER_NAME)
                response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
                pytest.assume(Httpx.getStatusCode(response) == 400)
            else:
                break
            count += 1

    # 用户Id字段效验
    def test_add_userid_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "用户Id值是NULL"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, None,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "用户Id为必填字段"})

    def test_add_userid_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "用户Id值是空字符"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, "", USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "用户Id为必填字段"})

    def test_add_userid_is_error(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "用户Id值是非法有效的"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        user_id = RandValue.getVerifi(8, 1)
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, user_id,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    # 用户名字字段效验
    def test_add_userno_is_null(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "用户名称值是NULL"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID, None)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "用户名称为必填字段"})

    def test_add_userno_is_null_char(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "用户名称名字值是空字符"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID, "")
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "用户名称为必填字段"})

    def test_add_userno_is_error(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "用户名称值是非法有效的"})
        title = AUTO + str(RandValue.getStr(RandValue.getInt("1,18"))).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        user_name = RandValue.getStr(8)
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     user_name)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN, json=data)
        pytest.assume(Httpx.getStatusCode(response) == 400)

    # 字段全都为空
    def test_add_all_is_error(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "所有字段值均为空"})
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, hook_header=AWEN_TOKEN,
                                 json=conversType(setAddSeckillActivity()))
        pytest.assume(Httpx.getContent(response) == {"msg": "请求参数格式有误"})

    # 无Token
    def test_add_not_token(self):
        setTag({"feature": "秒杀活动", "story": "创建新活动", "title": "无Token"})
        title = AUTO + str(RandValue.getStr(18)).title()
        begin_time = getSeckillActivityTime()
        end_time = Moment.computeDate(minutes=7, custom=begin_time)
        seckill_order_limit = RandValue.getInt("1,10000")
        is_shipping_free = 0
        data = setAddSeckillActivity(title, begin_time, end_time, seckill_order_limit, is_shipping_free, USER_ID,
                                     USER_NAME)
        conversType(data, ["user_id"])
        response = Httpx.sendApi(method="post", url=SECKILL_ADD_URL, json=data)
        pytest.assume(Httpx.getContent(response) == {"msg": "获取用户登录信息失败"})

