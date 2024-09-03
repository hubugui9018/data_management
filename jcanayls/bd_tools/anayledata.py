# coding=utf-8

import numpy as np

from scipy import stats
from sklearn import linear_model

reg = linear_model.LinearRegression()
reg.fit([[0,2,3],[1,3,0],[4,3,2]],[1,3,2])
print(reg.coef_)
print(reg.intercept_)

a = np.array([0.556,0.596,0.525,0.496,0.505,0.491,0.516])
mean,std = 155,12.4
sample_meam = a.mean()
se = std/np.sqrt(100)


Z = (sample_meam-mean)/se
P = 2*stats.norm.sf(abs(Z))
print(f"{Z:.4f} {P:.4f}")
P =2*stats.norm.cdf(abs(Z))

mean = np.random.randint(-10000, 10000)
std = 50
n = 50
all_ = np.random.normal(loc=mean, scale=std, size=10000)
sample = np.random.choice(all_, size=n)
sample_mean = sample.mean()
print(f"总体均值：{mean},样本均值：{sample_mean}")

se = std / np.sqrt(n)
min_ = sample_mean - 1.96 * se
max_ = sample_mean + 1.96 * se

print("置信区间（95%置信度）：", (min_, max_))


def m(m,b=2):
    pass

