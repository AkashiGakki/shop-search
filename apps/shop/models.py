from datetime import datetime

import mongoengine
from django.db import models

conn = mongoengine.connect('test')


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=200)
    price = models.FloatField()
    url = models.URLField(default='')
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name


class Tmall(models.Model):
    _id = models.CharField(max_length=200, primary_key=True)
    keyword = models.CharField(max_length=10)
    goods_url = models.URLField()
    image_url = models.URLField()
    goods_price = models.CharField(max_length=10)
    describe = models.TextField(max_length=500)
    shop = models.CharField(max_length=50)
    shop_url = models.URLField()

    def __str__(self):
        return self.keyword


class Test(mongoengine.Document):
    _id = mongoengine.StringField(primary_key=True)
    user_id = mongoengine.IntField()
    name = mongoengine.StringField()
    email = mongoengine.StringField()

    meta = {'collection': 'test'}
