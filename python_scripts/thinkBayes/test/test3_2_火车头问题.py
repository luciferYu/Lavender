#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 11:03
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# 火车头问题
# 铁路上以1到N命名火车头。有一天你看到一个标号60的火车头，请估计铁路上有多少火车头
# 基于这一观察结果，我们知道铁路上有60个或更多的火车头。但这个数字到底是多少
# 要应用贝叶斯进行推理，我们可以将这个问题分成两步进行：
# 1.在得到数据之前，我们对N的认识是什么？
# 2.已知一个N的任意值后，得到数据（“标志为60号的火车头”）的似然度？
#
# 第一个问题的答案就是问题的前置概率。第二个问题是似然度
#
# 在选择前置概率上，我们还没有太多的基本信息，但我们可以从一些简单情况开始
# 再考虑进一步的方法。 假设N可以是从1到1000等概率的任何值
hypos = range(1,1001)
# 接着我们需要的是一个似然度函数。
# 先假设存在一个有N个火车头的车队，我们看到60号火车头的概率是多少？
# 假设只有一个列车运营公司（或者只有一个我们关注的公司）
# 看到任意一个火车头有同等的可能，那么看到的任何特定火车头的机会是1/N

# 似然度函数如下
from thinkBayes.code.thinkbayes import Suite
class Train(Suite):
    def Likelihood(self, data, hypo):
        if hypo < data:
            return 0
        else:
            return 1.0/hypo

# Update 如下：
suite = Train(hypos)
suite.Update(60)
suite.Print()

# 因为有太多的假设（1000）要打印输出，所以所以挥着了图。意料之中的是N中60以下的所有值都被去掉了
# 如果非要猜测的话，最有可能的值是60。这似乎算不上很好的结果
# 毕竟，想想你恰好看到最高标志号火车头的机会是多少呢（应该不高吧）？
# 不过，如果想使猜到的答案完全正确的可能性最大化，你应该猜60

# 不过，这还不是我们的目标。另一个可选的方法是计算后验概率的平均值分布
def Mean(suite):
    total = 0
    for hypo,prob in suite.Items():
        total += hypo*prob
    return total

print(Mean(suite))
# 或者你可以由Pmf 提供的非常类似的方法
print(suite.Mean())
