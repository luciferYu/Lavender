#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 16:10
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com


from python_scripts.thinkBayes.code.thinkbayes import Suite
class M_and_M(Suite):
    # 我们可以使用Suite框架来解决M&M豆的问题。
    # 除了编写Likelihood 有点棘手，其他一切都很简单
    # 首先对1995年之前和之后的颜色混合情况进行封装
    mix94 = dict(brown=30,
                 yellow=20,
                 red=20,
                 green=10,
                 orange=10,
                 tan=10,
                 blue=0
                 )

    mix96 = dict(blue=24,
                 green=20,
                 orange=16,
                 yellow=14,
                 red=13,
                 brown=13)

    # 然后封装假设：
    hypoA = dict(bag1=mix94, bag2=mix96)  # 该假设表示第一袋是94年，第2袋是96年
    hypoB = dict(bag1=mix96, bag2=mix94)  # 该假设表示第一袋是96年，第2袋是94年

    # 接下来，从假设的名称来映射其含义
    hypotheses = dict(A=hypoA, B=hypoB)

    def Likelihood(self, data, hypo):
        bag,color = data
        mix = self.hypotheses[hypo][bag]
        like = mix[color]
        return like
#最后开始编写Likelihood 在这种情况下，假设是一个A或B的字符串，
#数据是一个指定了袋子年份和颜色的元组
suite = M_and_M('AB')
suite.Update(('bag1','yellow'))
suite.Update(('bag2','green'))
#suite.Update(('bag2','brown'))
suite.Print()