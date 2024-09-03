# -*- coding: utf-8 -*-
import pickle

from django.core.cache import cache


class RedisOps:
    # def __init__(self):
    #     pool = redis.ConnectionPool(host='172.16.13.78', port='6379', password='12345', decode_responses=False)
    #     self.rpool = redis.Redis(connection_pool=pool)

    def setRedisOpj(self, name, object, time):
        cache.set(name, pickle.dumps(object), time)

    def getRedisOpj(self, name):
        d = cache.get(name)
        if d != None:
            return pickle.loads(d)
        else:
            return []

    def setValue(self, name, value, time):
        cache.set(name, value, time)

    def getValue(self, name):
        return cache.get(name)

    def clearByName(self,name):
        cache.delete_pattern(name)