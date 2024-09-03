# -*-coding:utf-8 -*-
import time

from sklearn.linear_model import LinearRegression, Ridge
import pandas as pd
import numpy as np

class Tools:

    def compare_time(self,tm,other):
        s_time = time.mktime(time.strptime(tm, '%Y-%m-%d'))
        e_time = time.mktime(time.strptime(other, '%Y-%m-%d'))
        return int(s_time)-int(e_time)

    def bigdata(self):
        LinearRegression
        Ridge
        pass

