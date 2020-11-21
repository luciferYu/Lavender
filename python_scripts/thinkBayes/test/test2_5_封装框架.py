#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 16:03
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
from python_scripts.thinkBayes.code.thinkbayes import Pmf,Suite
# class Suite(Pmf):
#     '''代表一套假设及其概率'''
#
#     def __init__(self,hypos=tuple):
#         '''初始化分配'''
#
#     def Update(self,data):
#         '''更新基于该数据的每个假设'''
#
#     def Print(self):
#         '''打印出假设和他们的概率'''

# 要使用Suite对象 你应当编写一个继承自Suite的类，并自行提供Likelihood方法的实现
# 例如 蒙特大厅问题
class Monty(Suite):
    def Likelihood(self, data, hypo):
        if hypo == data:
            return 0
        elif hypo== 'A':
            return 0.5
        else:
            return 1

suite=Monty('ABC')
suite.Update('B')
suite.Print()