# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_add_product.py
# Author : YuYanQing
# Desc: 添加秒杀活动商品
# Date： 2021/8/23 11:20
'''
import pytest
from pytest_assume.plugin import assume
from iutils.OkHttps import Httpx
from iutils.AllureUtils import setTag
from iutils.RandUtils import RandValue
from testings.control.data import AWEN_TOKEN
from testings.control.url import SECKILL_PRODUCT_ADD_OR_EDIT_URL, SECKILL_PRODUCT_DELETE_URL
from testings.entity.Seckill import getSeckillUnderProduct, setSeckillProduct, selectActivity, selectActivityUnderGoods


class TestSeckillProduct():
    def test_on_start_activity_add_have_stock_not_mutual_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "未开始的活动-添加有库存/无互斥/且字段均合法的商品"})
        activity_id = selectActivity(1)[0]["id"]
        product = getSeckillUnderProduct(selectActivity(1)[0]["id"], 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        market_price = int(product["market_price"])
        price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                 promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            assert Httpx.getStatusCode(response) == 200

    def test_on_start_activity_add_seckill_price_eq_0_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "未开始的活动-添加有库存/无互斥/秒杀价为0的商品"})
        activity_id = selectActivity(1)[0]["id"]
        product = getSeckillUnderProduct(selectActivity(1)[0]["id"], 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=0, stock=stock,promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            assert Httpx.getStatusCode(response) == 400
            assert Httpx.getContent(response) == {"msg":"秒杀价为必填字段"}

    def test_on_start_activity_add_seckill_price_gt_market_price_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "未开始的活动-添加有库存/无互斥/秒杀价>市场价的商品"})
        activity_id = selectActivity(1)[0]["id"]
        product = getSeckillUnderProduct(selectActivity(1)[0]["id"], 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        price = int(product["market_price"])+1
        product_name = str(product["product_name"])
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            assert Httpx.getStatusCode(response) == 400
            assert Httpx.getContent(response) == {"msg":"请填写小于原售价的价格"}

    def test_on_start_activity_add_not_stock_not_mutual_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "未开始的活动-尝试添加无库存/无互斥的商品"})
        activity_id = selectActivity(1)[0]["id"]
        try:
            product = getSeckillUnderProduct(activity_id, 3)[0]
        except IndexError:
            raise IndexError("暂时没有改类型商品，请手动测试")
        else:
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            stock = int(product["stock"])
            product_name = str(product["product_name"])
            market_price = int(product["market_price"])
            price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
            stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                     promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,
                                     json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 400)
                pytest.assume(Httpx.getContent(response) == {"msg": "实际库存（0）不足"})

    def test_on_start_activity_goods_stock_eq0(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "未开始的活动-尝试添加无库存/无互斥的商品(但传入库存为0)"})
        activity_id = selectActivity(1)[0]["id"]
        try:
            product = getSeckillUnderProduct(activity_id, 3)[0]
        except IndexError:
            raise IndexError("暂时没有改类型商品，请手动测试")
        else:
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            product_name = str(product["product_name"])
            market_price = int(product["market_price"])
            price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=0,promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 400)
                pytest.assume(Httpx.getContent(response) == {"msg": "活动库存为必填字段"})

    def test_on_start_activity_add_not_stock_have_mutual_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "未开始的活动-尝试添加无库存/有互斥的商品"})
        activity_id = selectActivity(1)[0]["id"]
        product = getSeckillUnderProduct(activity_id, 2)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        market_price = int(product["market_price"])
        price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                 promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            pytest.assume(Httpx.getStatusCode(response) == 400)
            pytest.assume(Httpx.getContent(response) == {"msg": "该商品已参加其他促销-已参加秒杀活动"})

    def test_underway_activity_add_not_stock_not_mutual_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "进行中的活动-添加有库存/无互斥的商品"})
        activity_id = selectActivity(2)[0]["id"]
        product = getSeckillUnderProduct(activity_id, 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        market_price = int(product["market_price"])
        price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                 promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_underway_activity_add_seckill_price_eq_0_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "进行中的活动-添加有库存/无互斥/秒杀价为0的商品"})
        activity_id = selectActivity(2)[0]["id"]
        product = getSeckillUnderProduct(selectActivity(1)[0]["id"], 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=0, stock=stock,promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            assert Httpx.getStatusCode(response) == 400
            assert Httpx.getContent(response) == {"msg":"秒杀价为必填字段"}

    def test_underway_activity_add_seckill_price_gt_market_price_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "进行中的活动-添加有库存/无互斥/秒杀价>市场价的商品"})
        activity_id = selectActivity(2)[0]["id"]
        product = getSeckillUnderProduct(selectActivity(1)[0]["id"], 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        price = int(product["market_price"])+1
        product_name = str(product["product_name"])
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            assert Httpx.getStatusCode(response) == 400
            assert Httpx.getContent(response) == {"msg":"请填写小于原售价的价格"}

    def test_end_activity_add_not_stock_not_mutual_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "自然结束的活动-添加有库存/无互斥的商品"})
        activity_id = selectActivity(3)[0]["id"]
        product = getSeckillUnderProduct(activity_id, 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        market_price = int(product["market_price"])
        price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                 promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            pytest.assume(Httpx.getStatusCode(response) == 400)
            pytest.assume(Httpx.getContent(response) == {"msg": "该活动已经结束"})

    def test_terminat_activity_add_not_stock_not_mutual_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "手动终止的活动-添加有库存/无互斥的商品"})
        activity_id = selectActivity(4)[0]["id"]
        product = getSeckillUnderProduct(activity_id, 1)[0]
        sku_id = int(product["sku_id"])
        spu_id = int(product["spu_id"])
        stock = int(product["stock"])
        product_name = str(product["product_name"])
        market_price = int(product["market_price"])
        price = RandValue.getInt("1, 9") if market_price <= 10 else RandValue.getInt("1,%s" % (market_price))
        stock = RandValue.getInt("1, 9") if stock < 10 else RandValue.getInt("1,%s" % (stock))
        data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                 promotion_id=activity_id)
        response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN, json=data)
        with assume:
            pytest.assume(Httpx.getStatusCode(response) == 400)
            pytest.assume(Httpx.getContent(response) == {"msg": "该活动已经结束"})

    def test_underway_activity_edit_goods(self):
        setTag({"feature": "秒杀活动", "story": "添加商品", "title": "进行中的活动-删除-再次添加商品"})
        try:
            activity_id = selectActivity(2)[0]["id"]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            product = selectActivityUnderGoods(method="activity", activity_id=activity_id)[0]
            id = int(product["id"])
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            market_price = int(product["market_price"])
            product_name = str(product["product_name"])
            seckill_stock = int(product["seckill_stock"])
            price = RandValue.getInt("1,%s" % (market_price))
            stock = int(seckill_stock - seckill_stock / 2.5)
            delete = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_DELETE_URL, hook_header=AWEN_TOKEN,
                                   json={"id": id})
            with assume:
                pytest.assume(Httpx.getStatusCode(delete) == 200)
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                     promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,
                                     json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 200)

if __name__ == '__main__':
    TestSeckillProduct().test_underway_activity_add_not_stock_not_mutual_goods()
