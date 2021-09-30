# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： SeckillActivity.py
# Author : YuYanQing
# Desc: 秒杀活动公共类
# Date： 2021/8/26 9:08
'''

import math
from iutils.DateUtils import Moment
from iutils.OkHttps import Httpx
from iutils.Processor import JsonPath
from iutils.YamlUtils import YamlHandle
from testings.control.sql import connActivity
from testings.control.data import AWEN_TOKEN, ACTIVITY_WHITEL_LIST
from testings.control.path import SECKIL_LIST_PATH
from testings.control.url import SECKILL_LIST_URL, SECKILL_PRODUCT_SELECT_LIST_URL, MALL_PRODUCT_STOCK, \
    SECKILL_PRODUCT_LIST_URL


def setAddSeckillActivity(title=None, begin_time=None, end_time=None, seckill_order_limit=None, is_shipping_free=None,
                          user_id=None, user_name=None):
    """
    设置创建/编辑秒杀活动的请求参数
    :param title: * 活动标题
    :param begin_time: * 开始时间
    :param end_time:  * 结束时间
    :param seckill_order_limit: * 购买上限
    :param is_shipping_free: * 是否免运费
    :param user_id: * 用户id
    :param user_name: * 用户名称
    :return:
    """
    return {"title": title, "begin_time": begin_time, "end_time": end_time, "seckill_order_limit": seckill_order_limit,
            "is_shipping_free": is_shipping_free, "user_id": user_id, "user_name": user_name}


def setEditSeckillActivity(activity_id=None, title=None, begin_time=None, end_time=None, seckill_order_limit=None,
                           is_shipping_free=None,
                           user_id=None, user_name=None):
    """
    设置创建/编辑秒杀活动的请求参数
    :param activity_id:
    :param title: * 活动标题
    :param begin_time: * 开始时间
    :param end_time:  * 结束时间
    :param seckill_order_limit: * 购买上限
    :param is_shipping_free: * 是否免运费
    :param user_id: * 用户id
    :param user_name: * 用户名称
    :return:
    """
    return {"id": activity_id, "title": title, "begin_time": begin_time, "end_time": end_time,
            "seckill_order_limit": seckill_order_limit,
            "is_shipping_free": is_shipping_free, "user_id": user_id, "user_name": user_name}


def setStopSeckillActivity(id_=None, user_id=None, user_name=None):
    """
   设置停止秒杀活动的请求参数
   :param id: * 活动id
   :param user_id: * 用户id
   :param user_name: * 用户名称
   :return:
   """
    return {"id": id_, "user_id": user_id, "user_name": user_name}


def setSeckillList(status=None, title=None, page_index=None, page_size=None, order_by=None):
    """
    设置获取秒杀活动列表的参数
    :param status integer (query)活动状态： 1未开始 2进行中 3已结束 4已终止 ,如果要获取全部状态的活动
    :param title: string (query)	     活动名称
    :param page_index: integer (query) 当前多少页,从1开始 Default value : 1
    :param page_size:  integer (query)	 每页多少条数据
    :param order_by: integer (query)  排序顺序：1-创建时间倒序，2-创建时间升序

    """
    return {"status": status, "title": title, "page_index": page_index, "page_size": page_size, "order_by": order_by}


def getSeckillList(status, keyword, order_by="1"):
    """
    获取秒杀活动全部列表
    :param status
    :param keyword 搜索关键
    :param order_by 排序 默认倒序
    :return:
    """
    data = setSeckillList(status=status, page_index=1, page_size=15, order_by=order_by)
    response = Httpx.sendApi(method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN, params=data)
    if response.status_code == 200:
        YamlHandle.writeOjb(SECKIL_LIST_PATH, Httpx.getContent(response), "w")
        return JsonPath.find(Httpx.getContent(response), keyword)
    else:
        return None


# def getSeckillActivityTime():
#     """
#     获取有效的being_time 接口层
#     :return:
#     """
#     now_time = Moment.getTime("%Y-%m-%d %H:%M:%S")
#     is_start_end_time = getSeckillList(status=1, keyword="$.data..end_time")
#     is_underway_end_time = getSeckillList(status=2, keyword="$.data..end_time")
#     if is_start_end_time is not False and is_underway_end_time is not False:
#         unstart_end_time = sorted(is_start_end_time, reverse=True)[0] if len(is_start_end_time)>1 else is_start_end_time[0]
#         underway_end_time = sorted(is_underway_end_time, reverse=True)[0] if len(is_underway_end_time)>1 else is_underway_end_time[0]
#         if Moment.compareTime(unstart_end_time, underway_end_time) is True:
#             exist_end_time = unstart_end_time
#         else:
#             exist_end_time = underway_end_time
#         begin_time = Moment.computeDate(minutes=3, custom=exist_end_time)
#     elif is_start_end_time is not False and is_underway_end_time is False:
#         unstart_end_time = sorted(is_start_end_time, reverse=True)[0] if len(is_start_end_time)>1 else is_start_end_time[0]
#         begin_time = Moment.computeDate(minutes=3, custom=unstart_end_time)
#     elif is_start_end_time is False and is_underway_end_time is not False:
#         underway_end_time = sorted(is_underway_end_time, reverse=True)[0] if len(is_underway_end_time)>1 else is_underway_end_time[0]
#         begin_time = Moment.computeDate(minutes=3, custom=underway_end_time)
#     else:
#         begin_time = Moment.computeDate(minutes=3, custom=now_time)
#     return begin_time

def getSeckillActivityTime():
    """
    获取有效的being_time 数据层
    :return:
    """
    promotion = connActivity.callSql("select end_time from promotion order by end_time desc")
    exists_end_time = promotion.to_dict()["end_time"][0].strftime('%Y-%m-%d %H:%M:%S')
    if Moment.compareTime(exists_end_time, Moment.getTime("%Y-%m-%d %H:%M:%S")) is True:
        return Moment.computeDate(minutes=2, custom=exists_end_time)
    else:
        return Moment.computeDate(minutes=3, custom=Moment.getTime("%Y-%m-%d %H:%M:%S"))


def selectActivityInfo(keyword=None):
    """
    获取单条活动记录
    :param keyword: 条件
    :return:
    """
    return connActivity.callSql("select * from promotion {}".format(keyword))


def grepActivity(method, status):
    """
    过滤出不同状态下的活动
    :return:
    """
    white_activity =selectActivityInfo(keyword='where promotion.id {} (select promotion_product.promotion_id from promotion_product) and promotion.status = {} and promotion.id in {}'.format(method, status, tuple(ACTIVITY_WHITEL_LIST))).to_dict()
    if white_activity["id"] == {}:
        return selectActivityInfo(
            keyword='where promotion.id {} (select promotion_product.promotion_id from promotion_product) and promotion.status = {} and promotion.title like "{}"'.format(
                method, status, "%PY自动化%")).to_dict()
    elif white_activity["id"] !={}:
        return white_activity

def selectActivity(status, page_index=1, page_size=15):
    """
    获取所需状态下的秒杀活动信息
    :param update_status_list:
    :param method
    :param status
    :return:
    """
    data = Httpx.getContent(Httpx.sendApi(
        method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN,
        params=setSeckillList(status=status, page_index=page_index, page_size=page_size, order_by=1)))
    params = []
    total = math.ceil(data["total"] / 15)
    if total == 0:
        raise IndexError("{}-接口返回数据异常：{}，请先补充后再执行该Case".format(SECKILL_LIST_URL, data, status))
    for index in range(total):
        activity_list = Httpx.getContent(Httpx.sendApi(
            method="get", url=SECKILL_LIST_URL, hook_header=AWEN_TOKEN,
            params=setSeckillList(status=status, page_index=index + 1, page_size=page_size, order_by=1)))["data"]
        for activity in activity_list:
            if activity["status"] == status:
                params.append(activity)
    return params


def selectActivityUnderGoods(activity_id, method=None, page_index=1, page_size=15):
    """
    获取秒杀活动下的商品信息
    :param method
    :param activity_id
    :return:
    """
    url = SECKILL_PRODUCT_LIST_URL if method is "activity" else SECKILL_PRODUCT_SELECT_LIST_URL
    data = Httpx.getContent(Httpx.sendApi(
        method="get", url=url, hook_header=AWEN_TOKEN,
        params=setSeckillProductSearch(page_index=page_index, page_size=page_size, promotion_id=activity_id,
                                       product_name="", sku_id="", spu_id="")))
    params = []
    total = math.ceil(data["total"] / 15)
    if total == 0:
        raise IndexError("{}-接口返回数据异常：{}，请先补充后再执行该Case".format(url, data))
    for index in range(total):
        activity_list = Httpx.getContent(Httpx.sendApi(
            method="get", url=url, hook_header=AWEN_TOKEN,
            params=setSeckillProductSearch(page_index=index + 1, page_size=page_size, promotion_id=activity_id,
                                           product_name="", sku_id="", spu_id="")))["data"]
        for activity in activity_list:
            params.append(activity)
    return params

#
# def insertActivityProduct(spu_id, sku_id, promotion_id, types,
#                           channel_id, product_name, up_down_state,
#                           product_img, market_price, seckill_price, seckill_stock, create_time):
#     """
#     插入商品数据
#     :param spu_id:
#     :param sku_id:
#     :param promotion_id:
#     :param types:
#     :param channel_id:
#     :param product_name:
#     :param up_down_state:
#     :param product_img:
#     :param market_price:
#     :param seckill_price:
#     :param seckill_stock:
#     :param create_time:
#     :return:
#     """
#     connActivity.doSql('insert into promotion_product '
#                        '(spu_id, sku_id, promotion_id, types, channel_id, product_name, up_down_state, product_img, market_price, seckill_price, seckill_stock, create_time)'
#                        ' values {}'
#                        .format((spu_id, sku_id, promotion_id, types, channel_id, product_name, up_down_state,
#                                 product_img, market_price, seckill_price, seckill_stock, create_time)))


def setSeckillProduct(spu_id=None, product_name=None, sku_id=None, price=None, stock=None, promotion_id=None):
    """
    设置添加商品的请求参数
    :param spu_id: 	    产品spu id integer
    :param product_name: 产品名称 integer
    :param sku_id:      商品 sku id integer
    :param price:      秒杀价（单位分) integer
    :param stock:       秒杀活动库存 integer
    :param promotion_id:  活动id integer
    :return:
    """
    return {"spu_id": spu_id, "product_name": product_name, "sku_id": sku_id, "price": price,
            "stock": stock, "promotion_id": promotion_id}


def setSeckillProductSearch(page_index="1", page_size="15", promotion_id="", product_name="", sku_id="", spu_id="",
                            order_by=1):
    """
    设置可以参加秒杀活动的阿闻商城的商品参数
    :param page_index integer * (query)	当前多少页 从1开始
    :param page_size integer * (query)	每页多少条数据
    :param promotion_id integer * (query)	秒杀活动id
    :param product_name string (query)	商品名称
    :param sku_id integer (query)	商品sku id
    :param spu_id integer (query)	商品的产品id
    :param order_by 排序
    :return:
    """
    return {"page_index": page_index, "page_size": page_size, "promotion_id": promotion_id,
            "product_name": product_name,
            "spu_id": spu_id, "sku_id": sku_id, "order_by": order_by}


def getSeckillUnderProduct(activity_id, method):
    """
    获取有库存(可用/不可用）/无库存（可用/不可用）的活动商品
    :return:
    """
    data = Httpx.getContent(Httpx.sendApi(
        method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN,
        params=setSeckillProductSearch(page_index=1, page_size=15, promotion_id=activity_id,
                                       product_name="", sku_id="", spu_id="")))
    old_data = []
    for index in range(math.ceil(data["total"] / 15)):
        if len(old_data) < 3:  # 减少数据请求量 加快case执行熟读
            old_data += Httpx.getContent(Httpx.sendApi(
                method="get", url=SECKILL_PRODUCT_SELECT_LIST_URL, hook_header=AWEN_TOKEN,
                params=setSeckillProductSearch(page_index=index + 1, page_size=15, promotion_id=activity_id,
                                               product_name="", sku_id="", spu_id="")))["data"]
    available = []  # 可以用的商品（有库存、无互斥）
    not_stock_not_mutual = []  # 无库存 无互斥
    have_stock_have_mutual = []  # 有库存 互斥
    not_stock_have_mutual = []  # 无库存 互斥
    for index in range(len(old_data)):
        pending_data = selectStock(sku_id=old_data[index]["sku_id"])
        time_conflict = old_data[index]["time_conflict"]
        stock = pending_data["goods_info"]["ProductsInfo"][0]["stock"]
        old_data[index].update({"stock": stock})
        if stock <= 0 and time_conflict == 0:
            not_stock_not_mutual.append(old_data[index])
        elif stock > 0 and time_conflict == 0:
            available.append(old_data[index])
        elif stock > 0 and time_conflict == 1:
            have_stock_have_mutual.append(old_data[index])
        elif stock <= 0 and time_conflict == 1:
            not_stock_have_mutual.append(old_data[index])
    if method == int(1):
        return available
    elif method == int(2):
        return have_stock_have_mutual
    elif method == int(3):
        return not_stock_not_mutual
    elif method == int(5):
        return not_stock_have_mutual


def selectStock(sku_id, is_all_virtual=0, stock=0, type_=0, is_need_pull=0, source=1):
    """
    查询库存
    :param is_all_virtual:
    :param sku_id:
    :param stock:
    :param type_:
    :param is_need_pull:
    :param source:
    :return:
    """
    data = {"ProductsInfo": [{"child_ren": [], "finance_code": [], "is_all_virtual": is_all_virtual, "sku_id": sku_id,
                              "stock": stock, "type": type_}], "is_need_pull": is_need_pull, "source": source}
    return Httpx.getContent(Httpx.sendApi(method="post", url=MALL_PRODUCT_STOCK, hook_header=AWEN_TOKEN, json=data))


def doCommit(user_agent=3,channel_id=5,address_id=8316,shop_name="优宠商城官方自营",shop_id="1",privilege=0,freight=0,
    total=1,goods_total=1,buyer_memo="",tel_phone="18175699611",source=2,order_type=9,receiver_date_msg="",dis_id="",dis_type=0,
             first_order="0",order_promotions=[],product_id="",product_name="",sku="",price="",number="",image="",
             promotion_type="",promotion_id="",child_product_list=""):
    return {
        "order": {
            "user_agent": user_agent,
            "channel_id": channel_id,
            "address_id": address_id,
            "shop_name": shop_name,
            "shop_id": shop_id,
            "privilege": privilege,
            "freight": freight,
            "total": total,
            "goods_total": goods_total,
            "buyer_memo": buyer_memo,
            "tel_phone": tel_phone,
            "source": source,
            "order_type": order_type,
            "receiver_date_msg": receiver_date_msg,
            "dis_id": dis_id,
            "dis_type": dis_type,
            "first_order": first_order
        },
        "order_promotions": order_promotions,
        "order_products": [
            {
                "product_id": product_id,
                "product_name": product_name,
                "sku": sku,
                "price": price,
                "number": number,
                "image": image,
                "promotion_type": promotion_type,
                "promotion_id": promotion_id,
                "child_product_list": child_product_list
            }
        ]
    }
    
    
if __name__ == '__main__':
    # begin_time = Moment.computeDate(minutes=5, custom=getSeckillActivityTime())
    # end_time = Moment.computeDate(minutes=7, custom=begin_time)
    # print(begin_time,end_time)
    print(grepActivity(method="in", status=2))
    print(doCommit())
