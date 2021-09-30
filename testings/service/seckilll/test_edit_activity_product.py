# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_add_product.py
# Author : YuYanQing
# Desc: 修改秒杀活动商品
# Date： 2021/8/23 11:20
'''
import pytest
from pytest_assume.plugin import assume

from iutils.OkHttps import Httpx
from iutils.AllureUtils import setTag
from iutils.RandUtils import RandValue
from testings.control.data import AWEN_TOKEN
from testings.control.url import SECKILL_PRODUCT_ADD_OR_EDIT_URL
from testings.entity.Seckill import setSeckillProduct, selectActivity, selectActivityUnderGoods


class TestSeckillProduct():
    def test_on_start_activity_edit_goods(self):
        setTag({"feature": "秒杀活动", "story": "编辑商品信息", "title": "未开始的活动编辑商品"})
        try:
            activity_id = selectActivity(1)[0]["id"]
            product = selectActivityUnderGoods(method="activity", activity_id=activity_id)[0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            product_name = str(product["product_name"])
            seckill_stock = int(product["seckill_stock"])
            market_price = int(product["market_price"])
            price = RandValue.getInt("1,%s" % (market_price))
            stock = int(seckill_stock - seckill_stock / 3.5)
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                     promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,
                                     json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 200)

    def test_underway_activity_edit_goods(self):
        setTag({"feature": "秒杀活动", "story": "编辑商品信息", "title": "进行中的活动编辑商品"})
        try:
            activity_id = selectActivity(2)[0]["id"]
            product = selectActivityUnderGoods(method="activity", activity_id=activity_id)[0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            product_name = str(product["product_name"])
            seckill_stock = int(product["seckill_stock"])
            market_price = int(product["market_price"])
            price = RandValue.getInt("1,%s" % (market_price))
            stock = int(seckill_stock - seckill_stock / 3.5)
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                     promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,
                                     json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 400)
                pytest.assume(Httpx.getContent(response) == {"msg":"只有未开始的活动商品才可以编辑"})

    def test_end_activity_edit_goods(self):
        setTag({"feature": "秒杀活动", "story": "编辑商品信息", "title": "自然结束的活动编辑商品"})
        try:
            activity_id = selectActivity(3)[0]["id"]
            product = selectActivityUnderGoods(method="activity", activity_id=activity_id)[0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            product_name = str(product["product_name"])
            seckill_stock = int(product["seckill_stock"])
            market_price = int(product["market_price"])
            price = RandValue.getInt("1,%s" % (market_price))
            stock = int(seckill_stock - seckill_stock / 3.5)
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                     promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,
                                     json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 400)
                pytest.assume(Httpx.getContent(response) == {"msg": "该活动已经结束"})

    def test_terminat_activity_edit_goods(self):
        setTag({"feature": "秒杀活动", "story": "编辑商品信息", "title": "手动终止的活动编辑商品"})
        try:
            activity_id = selectActivity(4)[0]["id"]
            product = selectActivityUnderGoods(method="activity", activity_id=activity_id)[0]
        except AttributeError:
            raise AttributeError("暂时没有可用数据-需手动构建")
        else:
            sku_id = int(product["sku_id"])
            spu_id = int(product["spu_id"])
            product_name = str(product["product_name"])
            seckill_stock = int(product["seckill_stock"])
            market_price = int(product["market_price"])
            price = RandValue.getInt("1,%s" % (market_price))
            stock = int(seckill_stock - seckill_stock / 3.5)
            data = setSeckillProduct(spu_id=spu_id, product_name=product_name, sku_id=sku_id, price=price, stock=stock,
                                     promotion_id=activity_id)
            response = Httpx.sendApi(method="post", url=SECKILL_PRODUCT_ADD_OR_EDIT_URL, hook_header=AWEN_TOKEN,
                                     json=data)
            with assume:
                pytest.assume(Httpx.getStatusCode(response) == 400)
                pytest.assume(Httpx.getContent(response) == {"msg": "该活动已经结束"})


if __name__ == '__main__':
    TestSeckillProduct().test_terminat_activity_edit_goods()
