# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_edit_products.py
# Author : YuYanQing
# Desc: 编辑商品
# Date： 2021/8/19 17:17
'''
import random

import pytest

from iutils.AllureUtils import setTag
from iutils.DateUtils import Moment
from iutils.OkHttps import Httpx
from iutils.Processor import JsonPath
from iutils.RandUtils import RandValue
from testings.control.data import AWEN_TOKEN, CATEGORYID
from testings.control.init import Envision
from testings.control.url import CREATE_PRODUCT_URL
from testings.entity.Backend import joinEditProductInfo, getMediaItem

config = Envision.getYaml("boss_product_new.yaml")['config']
test_setup = Envision.getYaml("boss_product_new.yaml")['test_setup']

class TestEditProduct():
    # 商品名称
    def test_edit_product_name(self):
        setTag({'feature':'阿闻平台修改商品信息','story': '修改商品名称','title':'正常修改名称'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "name":
                old_data["product"].update(
                    {key: str(value).replace("Edit", "") + "Edition"}
                    if "Edit" in str(value) else {key: str(value).replace("Edition", "") + "Edit"})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":200,"message":"","error":"","details":None})

    def test_edit_lack_goods_name(self):
        setTag({'feature': '阿闻平台修改商品信息', 'story': '修改商品名称', 'title': '缺少商品名称字段'})
        old_data = joinEditProductInfo()
        old_data["product"].pop("name")
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":400,"message":"商品名称不能为空","error":"","details":None})

    def test_edit_goods_name_is_null(self):
        setTag({'feature': '阿闻平台修改商品信息', 'story': '修改商品名称', 'title': '商品名称是Null值'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "name":
                old_data["product"].update({key: None})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":400,"message":"商品名称不能为空","error":"","details":None})

    def test_edit_goods_name_is_null_character(self):
        setTag({'feature': '阿闻平台修改商品信息', 'story': '修改商品名称', 'title': '商品名称是空字符'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "name":
                old_data["product"].update({key: ""})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":400,"message":"商品名称不能为空","error":"","details":None})

    def test_edit_goods_name_is_cross(self):
        setTag({'feature': '阿闻平台修改商品信息', 'story': '修改商品名称','title': '商品名称字符长度越界'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "name":
                update_value = RandValue.getStr(256)
                old_data["product"].update({key: update_value})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getStatusCode(response)==400)


    # 商品分类
    def test_edit_goods_sort(self):
        setTag({'feature':'阿闻平台修改商品信息','story': '修改商品分类','title': '正常修改商品分类'})
        category_id = int(random.sample(JsonPath.find(CATEGORYID, "$.details..id"), 1)[0])
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "category_id":
                old_data["product"].update({key: category_id})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":200,"message":"","error":"","details":None})

    def test_edit_goods_sort_is_null(self):
        setTag({'feature':'阿闻平台修改商品信息','story': '修改商品分类','title': '商品分类为空'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "category_id":
                old_data["product"].update({key: None})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={'code': 400, 'message': '商品分类不能为空', 'error': '', 'details': None})

    def test_edit_lack_goods_sort(self):
        setTag({'feature':'阿闻平台修改商品信息','story': '修改商品分类','title': '缺少商品分类字段'})
        old_data = joinEditProductInfo()
        old_data["product"].pop("category_id")
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={'code': 400, 'message': '商品分类不能为空', 'error': '', 'details': None})

    def test_edit_goods_sort_is_null_character(self):
        setTag({'feature':'阿闻平台修改商品信息','story': '修改商品分类','title': '商品分类为空字符'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "category_id":
                old_data["product"].update({key: ""})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":400,"message":"code=400, message=Unmarshal type error: expected=int32, got=string, field=product.category_id, offset=45, internal=json: cannot unmarshal string into Go struct field Product.product.category_id of type int32","error":"","details":None})

    def test_edit_goods_sort_is_cross(self):
        setTag({'feature':'阿闻平台修改商品信息','story': '修改商品分类','title': '商品分类数组长度越界'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            update_value = RandValue.getStr(12)
            if key == "category_id":
                old_data["product"].update({key: update_value})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getStatusCode(response)==400)

    # 商品货号
    def test_edit_good_third_sku_id(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品货号','title': '第三方货号重复'})
        old_data = joinEditProductInfo()
        third_sku_id = str(Moment.getTime("10timestamp"))
        for key, value in old_data["sku_info"][0].items():
            if key == "sku_third":
                for index in range(len(value)):
                    for k,v in value[index].items():
                        value[index].update({"third_sku_id":third_sku_id})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code": 400, "message": "第三方货号不能重复", "error": "", "details": None})

    # 商品条码信息
    def test_edit_good_bar_code(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品条码信息','title': '正常修改商品条码'})
        old_data = joinEditProductInfo()
        bar_code = int(RandValue.getInt("55,718")) + int(Moment.getTime("10timestamp"))
        for key, value in old_data["sku_info"][0].items():
            if key =="bar_code":
                old_data["sku_info"][0].update({"bar_code":str(bar_code)})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":200,"message":"","error":"","details":None})

    def test_edit_good_bar_code_is_null(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品条码信息','title': '商品条码信息为空'})
        old_data = joinEditProductInfo()
        for key, value in old_data["sku_info"][0].items():
            if key =="bar_code":
                old_data["sku_info"][0].update({"bar_code":None})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={'code': 400, 'message': '条码信息不能为空或为0', 'error': '', 'details': None})

    def test_edit_lack_good_bar_code_is_cross(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品条码信息','title': '商品条码信息数组越界'})
        old_data = joinEditProductInfo()
        bar_code = RandValue.getNum(37)
        for key, value in old_data["sku_info"][0].items():
            if key =="bar_code":
                old_data["sku_info"][0].update({"bar_code":bar_code})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getStatusCode(response)==400)

    def test_rear_good_pic(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品图片地址','title': '二次重组源数据的图片的顺序'})
        old_data = joinEditProductInfo()
        pic_list = JsonPath.find(joinEditProductInfo(), "$.product.pic")[0].split(",")
        pic = ",".join(random.sample(pic_list, 5))
        for key, value in old_data["product"].items():
            if key == "pic":
                old_data["product"].update({"pic":str(pic)})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":200,"message":"","error":"","details":None})

    def test_edit_good_pic(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品图片地址','title': '正常修改图片新图片'})
        old_data = joinEditProductInfo()
        mediaitem = getMediaItem(page_index=random.randint(20, 30))
        pic = ",".join(random.sample(mediaitem, 5))
        for key, value in old_data["product"].items():
            if key == "pic":
                old_data["product"].update({"pic":str(pic)})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={"code":200,"message":"","error":"","details":None})


    def test_edit_lack_good_pic(self):
        setTag({'feature':'阿闻平台修改商品信息','story':'修改商品图片地址','title': 'pic值是None'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "pic":
                old_data["product"].update({"pic":None})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN,json=old_data)
        pytest.assume(Httpx.getContent(response)=={'code': 400, 'message': '商品图片不能为空', 'error': '', 'details': None})

    def test_edit_lack_good_pic(self):
        setTag({'feature': '阿闻平台修改商品信息', 'story': '修改商品图片地址', 'title': 'pic值是空字符'})
        old_data = joinEditProductInfo()
        for key, value in old_data["product"].items():
            if key == "pic":
                old_data["product"].update({"pic": ""})
        response = Httpx.sendApi(method="post", url=CREATE_PRODUCT_URL, aided=True, hook_header=AWEN_TOKEN, json=old_data)
        pytest.assume(Httpx.getContent(response) == {'code': 400, 'message': '商品图片不能为空', 'error': '', 'details': None})
