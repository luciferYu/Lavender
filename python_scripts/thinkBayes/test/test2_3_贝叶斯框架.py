#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 17:22
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
from python_scripts.thinkBayes.code.thinkbayes import Pmf
class Cookie(Pmf):
    def __init__(self,hypos):
        '''给每个假设赋予相同的先验概率'''
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo,1)
        self.Normalize()

    mixes = {
        'Bowl1': dict(vanilla=0.75, chocolate=0.25),
        'Bowl2': dict(vanilla=0.5, chocolate=0.5)
    }

    def Likelihood(self,data,hypo):
        mix = self.mixes[hypo]
        like = mix[data]
        return like

    def Update(self,data):
        for hypo in self.Values():
            like = self.Likelihood(data,hypo)
            self.Mult(hypo,like)
        self.Normalize()



if __name__ == '__main__':
    hypos=['Bowl1','Bowl2']
    pmf = Cookie(hypos)
    pmf.Update('vanilla')
    for hypo,prob in pmf.Items():
        print(hypo,prob)

    dataset = ['vanilla','chocolate','vanilla'] # 再次从碗中拿取3块饼干 更新概率分布
    for data in dataset:
        pmf.Update(data)

    for hypo,prob in pmf.Items():
        print(hypo,prob)