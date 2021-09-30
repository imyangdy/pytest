# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
'''
# FileName： Backend.py
# Author : YuYanQing
# Desc: 阿闻管理后台公共模块
# Date： 2021/7/5 11:37
'''
import os
import random
from BaseSetting import Route
from iutils.DateUtils import Moment
from iutils.Loader import Loader
from iutils.OkHttps import Httpx
from iutils.Processor import JsonPath
from iutils.RandUtils import RandValue
from iutils.Template import Template
from iutils.YamlUtils import YamlHandle
from testings.control.data import AWEN_TOKEN, CATEGORYID, USER_INFO, NEWSUCCED
from testings.control.path import MEDI_AITEM_PATH, CATEGORY_PATH, CHANNEL_CATEGORY_PATH, IMG_PATH
from testings.control.url import  MEDIA_ITEM_URL, MED_IAITEM_UPLOAD_URL, CATEGORY_LIST_URL, \
    PRODUCT_LIST_URL, CHANNEL_PRODUCT_LIST_URL, STORE_INFO_URL, COPY_CHANNEL_URL, CHANNEL_UP_URL, CHANNEL_STATUS_REFRESH_URL, \
    PRODUCT_TAGS_URL, PRODUCT_EDIT_QUERY_URL, CHANNEL_PRODUCT_EDIT_QUERY_URL


# 商品中心
def setVirtualProduct(category_id=None, name=None, pic=None, selling_point=None, term_value=None,
                      market_price=None,
                      retail_price=None, content_pc=None):
    """
    设置创建虚拟商品请求参数
    :param category_id: 分类id
    :param name:  商品名称
    :param pic:   商品主图
    :param selling_point: 副标题
    :param term_value:  时间
    :param market_price: 销售价
    :param retail_price: 市场价
    :param content_pc:   PC侧推荐图
    :return:
    """
    temp = {"category_id": category_id, "name": name, "pic": pic, "selling_point": selling_point,
            "term_value": term_value, "market_price": market_price, "retail_price": retail_price,
            "content_pc": content_pc}
    name = "258-PY虚拟商品"
    mediaitem = getMediaItem(page_index=random.randint(1, 20))
    pic = ",".join(random.sample(mediaitem, 5))
    spec_pic = ",".join(random.sample(mediaitem, 1))
    content_pc = RandValue.getStr(50)
    term_value = Moment.getTime("10timestamp")
    market_price = RandValue.getInt("55,718")
    retail_price = RandValue.getInt("1,55")
    category_id = int(random.sample(JsonPath.find(CATEGORYID, "$.details..id"), 1)[0])
    replace_data = {"category_id": category_id, "name": name, "pic": pic,
                    "selling_point": selling_point, "term_value": term_value,
                    "market_price": market_price, "retail_price": retail_price, "content_pc": content_pc,
                    "spec_pic": spec_pic}
    for k, v in temp.items():
        if v is not None:
            replace_data.update({k: v})
    general_data = Loader.jsonFile(Route.joinPath("test_json", "create_virtual_product.json"))
    req_data = Template(general_data).subStitute(replace_data)
    return req_data


def setSampleProduct(category_id=None, name=None, pic=None, selling_point=None, term_value=None,
                     market_price=None,
                     retail_price=None, a8_third_sku_id=None, zl_third_sku_id=None, gy_third_sku_id=None,
                     bar_code=None, content_pc=None):
    """
    设置创建实物商品请求参数
    :param category_id: 分类id
    :param name:  商品名称
    :param pic:   商品主图
    :param selling_point: 副标题
    :param term_value:  时间
    :param market_price: 销售价
    :param retail_price: 市场价
    :param content_pc:   PC侧推荐图
    :param bar_code:  条形编码
    :param gy_third_sku_id: 管易货号
    :param zl_third_sku_id: 子龙货号
    :param a8_third_sku_id: a8货号
    :return:
    """
    temp = {"category_id": category_id, "name": name, "pic": pic, "selling_point": selling_point,
            "term_value": term_value, "market_price": market_price, "retail_price": retail_price,
            "a8_third_sku_id": a8_third_sku_id, "zl_third_sku_id": zl_third_sku_id,
            "gy_third_sku_id": gy_third_sku_id, "bar_code": bar_code, "content_pc": content_pc}
    mediaitem = getMediaItem(page_index=random.randint(1, 20))
    pic = ",".join(random.sample(mediaitem, 5))
    spec_pic = ",".join(random.sample(mediaitem, 1))
    content_pc = RandValue.getStr(50)
    uuid = RandValue.getUuid().split("-")[0]
    a8_third_sku_id = zl_third_sku_id = gy_third_sku_id = int(Moment.getTime("10timestamp"))
    category_id = int(random.sample(JsonPath.find(CATEGORYID, "$.details..id"), 1)[0])
    market_price = RandValue.getInt("55,718")
    retail_price = RandValue.getInt("1,55")
    bar_code = int(RandValue.getInt("55,718")) + int(Moment.getTime("10timestamp"))
    name = "258-PY实物商品" + str(uuid)
    replace_data = {"category_id": category_id, "name": name, "pic": str(pic),
                    "selling_point": name, "term_value": term_value,
                    "market_price": market_price, "retail_price": retail_price,
                    "a8_third_sku_id": str(RandValue.getInt("55,718")) + str(a8_third_sku_id),
                    "zl_third_sku_id": str(RandValue.getInt("55,718")) + str(int(zl_third_sku_id / 100) + 5),
                    "gy_third_sku_id": str(RandValue.getInt("55,718")) + str(int((gy_third_sku_id / 105) + 10)),
                    "bar_code": bar_code,
                    "content_pc": content_pc, "spec_pic": spec_pic}
    for k, v in temp.items():
        if v is not None:
            replace_data.update({k: v})
    # ToDo 也可以在定义量中处理掉null值改怎么插入 DataKit暂时打了补丁实现了功能
    general_data = Loader.jsonFile(Route.joinPath("test_json", "create_sample_product.json"))
    return Template(general_data).subStitute(mapping=replace_data,
                                             disable_data=["third_sku_id", "bar_code"])


def setSearchProduct(page_index=1, page_size=10, product_type=None, is_del=None,
                     where=None, where_type="third_spu_sku_id", total_count=None,
                     is_gj=0, channel_id="", up_down_state=None):
    """
    设置搜索商品请求参数
    :param page_index: 下标
    :param page_size:   分页量
    :param product_type: 商品类型
    :param is_del:   是否被删除（回收站）
    :param id_del:   是否可用
    :param where:    具体内容
    :param where_type: 模糊查询 name product_id third_spu_sku_id sku_id
    :param total_count:
    :param is_gj: 区分管家
    :param channel_id:  渠道id
    :param up_down_state:  是否上架
    :return:
    """
    return {"page_index": page_index, "page_size": page_size, "product_type": product_type, "is_del": is_del,
            "where": where, "where_type": where_type, "total_count": total_count,
            "is_gj": is_gj, "channel_id": channel_id, "up_down_state": up_down_state}


def setOrderList(search_type=None, keyword=None, time_type=None, start_time=None, end_time=None,
                 product_name=None, order_status=None, channel_id=None, order_type=None, delivery_type=None,
                 pay_mode=None,
                 app_channel=None, page_index=None, page_size=None, order_list_type=None, paysn=None,
                 sale_channel=None):
    """
    设置订单搜索的请求参数
    :param search_type: 订单搜索类型
    全部（0~6 全部、订单号、外部单号、收货人姓名、收货人手机号、买家手机号、店铺名称）
    实物/虚拟（0~4 全部、子订单号、父订单号、外部单号、手机号）
    :param keyword: 搜索类型具体的键值
    :param time_type:  时间段 0~1 下单时间、完成时间
    :param start_time: 开始时间
    :param end_time:   结束时间
    :param product_name:  商品名称
    :param order_status:  订单状态20101~20107 全部（0）、未接单、已接单、配送中、已送达、已完成、已取货、已取消
    :param channel_id:    渠道 1~4 420
    :param order_type:    订单类型1~3 全部、普通订单、预订订单
    :param delivery_type: 配送方式0~4 全部、快递、外卖、自提、同城送
    :param pay_mode:     支付方式0~8 全部、支付宝、微信、美团、其他、饿了么、京东支付、储值卡
    :param app_channel:  店铺类型 0~3 全部、新瑞鹏、TP代运营
    :param page_index:   分页start值
    :param page_size:    分页量
    :param order_list_type: 订单类型 1~3 全部订单 实物订单 虚拟订单
    :param paysn:        订单号
    :param sale_channel: 销售渠道 0~7 全部、Android、iOS、小程序、公众号、Web、竖屏、其他
    :return:
    """
    return {"search_type": search_type, "keyword": keyword, "time_type": time_type, "start_time": start_time,
            "end_time": end_time,
            "product_name": product_name, "order_status": order_status, "channel_id": channel_id,
            "order_type": order_type, "delivery_type": delivery_type, "pay_mode": pay_mode,
            "app_channel": app_channel,
            "page_index": page_index, "page_size": page_size, "order_list_type": order_list_type,
            "paysn": paysn, "sale_channel": sale_channel
            }

def getMediaItem(aclass_id="1", media_type="1", page_index=1, page_size=15):
    """
    设置获取主图的请求参数
    :param aclass_id:  string
    :param media_type: integer 文件类型1图片 2媒体库
    :param page_index: integer 下标
    :param page_size:  integer 分页数量
    :return:
    """
    data = {"aclass_id": aclass_id, "media_type": media_type, "page_index": page_index, "page_size": page_size}
    resp = Httpx.getContent(Httpx.sendApi(method="post", url=MEDIA_ITEM_URL, data=data, hook_header=AWEN_TOKEN))
    YamlHandle.writeOjb(file_path=MEDI_AITEM_PATH, data=resp, method="w")
    return JsonPath.find(resp, "$.media_item_class..apic_path")


def uploadMediaItem():
    """

    :return:
    """
    file_path = os.path.join(IMG_PATH, "".join(random.sample(os.listdir(IMG_PATH), 1)))
    resp = Httpx.getContent(Httpx.uploadFile(method="single", url=MED_IAITEM_UPLOAD_URL, file_path=file_path))
    print(resp)


def getCategory(from_=None, page_index=1, page_size=10, total_count=0, data_type="category_sub", parent_id=""):
    """
    获取商品分类
    :param from_: 来源
    :param page_index:
    :param page_size:
    :param total_count:
    :param data_type:
    :param parent_id:
    :return:
    """
    if from_ is None:
        try:
            data = {"page_index": page_index, "page_size": page_size, "total_count": total_count,
                    "data_type": data_type, "parent_id": parent_id}
            resp = Httpx.getContent(
                Httpx.sendApi(method="get", url=CATEGORY_LIST_URL, data=data, hook_header=AWEN_TOKEN))
            YamlHandle.writeOjb(file_path=CATEGORY_PATH, data=resp, method="w")
        except Exception:
            try:
                resp = Loader.yamlFile(file_path=CATEGORY_PATH)
            except Exception:
                raise Exception("请求平台商品分类失败,兜底数据加载失败")
        return JsonPath.find(resp, "$.details..id")
    else:
        try:
            data = {"page_index": page_index, "page_size": page_size, "total_count": total_count,
                    "data_type": data_type, "parent_id": parent_id}
            resp = Httpx.getContent(
                Httpx.sendApi(method="get", url=CATEGORY_LIST_URL, data=data, hook_header=AWEN_TOKEN))
            YamlHandle.writeOjb(file_path=CHANNEL_CATEGORY_PATH, data=resp, method="w")
        except Exception:
            try:
                resp = Loader.yamlFile(file_path=CHANNEL_CATEGORY_PATH)
            except Exception:
                raise Exception("请管家商品分类失败,兜底数据加载失败")
        return JsonPath.find(resp, "$.details..id")


def getProductList(from_: str, channel_id=None, where: str = None, where_type: str = None, is_del=None,
                   up_down_state=None, product_type=None) -> dict:
    """
    获取商品列表
    :param from_
    :param is_del: 是否在回收站
    :param product_type: 商品类型
    :param up_down_state: 是否上架
    :param where 搜索键值
    :param channel_id: 渠道id
    :param where_type: 搜索类型 name product_id third_spu_sku_id sku_id
    :return:
    """
    if from_ == "platform":  # 平台
        url = PRODUCT_LIST_URL
        params = setSearchProduct(where=where, where_type=where_type, is_del=is_del,
                                  product_type=1 if product_type is not None else product_type)
    elif from_ == "steward":  # 管家
        url = PRODUCT_LIST_URL
        params = setSearchProduct(where=where, where_type=where_type, is_gj=1, is_del=is_del,
                                  product_type=1 if product_type is not None else product_type)
    elif from_ == "channel":  # 渠道
        url = CHANNEL_PRODUCT_LIST_URL
        params = setSearchProduct(channel_id=1 if channel_id is None else channel_id, where=where,
                                  where_type=where_type, is_del=is_del, up_down_state=up_down_state,
                                  product_type=1 if product_type is not None else product_type)
    return Httpx.getContent(
        Httpx.sendApi(method="get", url=url, hook_header=AWEN_TOKEN, headers={"userNo": getUser("name")},
                      params=params))

def getUser(method=None):
    if method == "id":
        try:
            params = USER_INFO["userNo"]
        except TypeError:
            params = "U_3B43GEA"  # 固定值 切换环境也需要换 没有的话会报错
    elif method == "name":
        try:
            params = USER_INFO["userName"]
        except TypeError:
            params = "yuyq"  # 固定值 切换环境也需要换 没有的话会报错
    return params


def getStoreInfo(channel_id: str = None, finance_code: str = None) -> dict:
    """
    获取阿闻后台的店铺信息
    :param channel_id
    :param finance_code
    :return:
    """
    try:
        headers = {"userNo": USER_INFO["userNo"]}
    except TypeError:
        headers = {"userNo": "U_3B43GEA"}  # 固定值 切换环境也需要换 没有的话会报错
    params = {"channel_id": 1, "finance_code": "CX0004"} if finance_code is None else {"channel_id": channel_id,
                                                                                       "finance_code": finance_code}
    return Httpx.getContent(Httpx.sendApi(method="get", url=STORE_INFO_URL, headers=headers, params=params))


def getProductEditQuery(from_, sku_id, channel_id=None, finance_code=None):
    """
    获取阿闻后台商品编辑时的信息
    :param from_: 来源
    :param sku_id 商品Id
    :param finance_code: 财务编码
    :param channel_id:   渠道Id
    :return:
    """
    if from_ == "platform":  # 平台
        url = PRODUCT_EDIT_QUERY_URL
        return Httpx.getContent(Httpx.sendApi(method="get", url=url, params={"id": sku_id}))
    elif from_ == "steward":  # 管家
        url = PRODUCT_EDIT_QUERY_URL
        return Httpx.getContent(Httpx.sendApi(method="get", url=url, params={"id": sku_id}))
    elif from_ == "channel" and int(channel_id) in (1, 2, 3, 4):  # 目前只兼容四个渠道
        url = CHANNEL_PRODUCT_EDIT_QUERY_URL
        params = {"id": sku_id, "channel_id": channel_id, "finance_code": finance_code}
        return Httpx.getContent(Httpx.sendApi(method="get", url=url, params=params))
    else:
        raise Exception("请先检查字段是否正确")


def copyChannel(product_id, channel_id, is_batch):
    """
    商品认领
    :return:
    """
    params = {"product_id": product_id, "channel_id": channel_id, "is_batch": is_batch}
    return Httpx.getContent(Httpx.sendApi(method="get", url=COPY_CHANNEL_URL, params=params))


def proStatusRefresh(from_, product_id=None, channel_id=None, finance_code=None,
                     category=None, operate_type=None, up_down_state=None):
    """
    刷新商品上架状态
    :param operate_type:
    :param category: 门店类型 3 门店仓 4 前置仓
    :param from_:
    :param product_id: 商品id
    :param channel_id: 渠道ID 只能一个一个来 list不行
    :param up_down_state: 上下架状态，1上架，0下架
    :param finance_code: 上架门店财务编码，多个财务编码用英文逗号分隔
    :return:
    """
    params = {"product_id": product_id, "channel_id": channel_id, "category": category,
              "up_down_state": up_down_state, "operate_type": operate_type}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    if finance_code is not None:
        params.update({"finance_code": finance_code, "finance_code_list": finance_code, "is_all_finance": 0})
    else:
        params.update({"finance_code": "", "is_all_finance": 1})
    if from_ == "up":
        return Httpx.getContent(
            Httpx.sendApi(method="post", hook_header=AWEN_TOKEN, headers=headers, url=CHANNEL_UP_URL, data=params))
    elif from_ == "down":
        return Httpx.getContent(
            Httpx.sendApi(method="post", hook_header=AWEN_TOKEN, headers=headers, url=CHANNEL_STATUS_REFRESH_URL,
                          data=params))


def getTags(sku_id):
    """
    获取编辑阿闻平台商品时的Tag规格信息
    :return:
    """
    return Httpx.getContent(
        Httpx.sendApi(method="get", hook_header=AWEN_TOKEN, url=PRODUCT_TAGS_URL, params={"sku_id": sku_id}))


def joinEditProductInfo():
    """
    重组编辑商品信息时的原始数据
    :return:
    """
    third_sku_id = JsonPath.find(NEWSUCCED, "$.sku_info..third_sku_id")[0]
    product_info = getProductList(from_="platform", where=random.sample(third_sku_id, 1), where_type="third_spu_sku_id")
    product_ids = JsonPath.find(product_info, "$.details.[0].id")
    product_tags = JsonPath.find(getTags(product_ids[1]), "$.data.[0]")[0]
    edit_infos = getProductEditQuery(from_="platform", sku_id=product_ids[0])
    product = JsonPath.find(edit_infos, "$.product.")[0]
    sku_group = JsonPath.find(edit_infos, "$.sku_group.")
    sku_info = JsonPath.find(edit_infos, "$.sku_info.")[0]
    product_attr = JsonPath.find(edit_infos, "$.product_attr.")[0]
    return {"product": product, "product_attr": product_attr, "sku_group": sku_group, "sku_info": sku_info,
            "product_tags": product_tags}


if __name__ == '__main__':
    # print(getMediaItem())
    # print(getCategory(from_="channel"))
    # print(getProductList(from_="platform", where="1023995", where_type="id"))
    # print(getProductList(from_="steward", where="1023995", where_type="id"))
    # print(getProductList(from_="channel", where="1023995", where_type="id"))
    # print(getStoreInfo())
    # print(getStoreList())
    # print(getStoreDetail())
    # print(getProductEditQuery(from_="platform", sku_id="1023995"))
    # print(getProductEditQuery(from_="steward", sku_id="1023995"))
    # print(getProductEditQuery(from_="channel", sku_id="1023995", channel_id="1"))
    # print(copyChannel(channel_id="1,2,3,4", product_id="1023995", is_batch="flase"))
    # print(proStatusRefresh(from_="up", product_id="1023995", channel_id="1", finance_code="CX0001,CX0011", category=4))
    # print(getTags("1030123001"))
    print(joinEditProductInfo())