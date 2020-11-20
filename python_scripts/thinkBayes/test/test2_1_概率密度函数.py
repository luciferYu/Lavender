#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 16:50
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
#from ..code.thinkbayes import Pmf
from python_scripts.thinkBayes.code.thinkbayes import Pmf
# pmf为概率密度函数
pmf = Pmf()
for x in [1,2,3,4,5,6]:
    pmf.Set(x,1/6.0)

s = '''Wikipedia is a Web-based, free-content encyclopedia written collaboratively by volunteers and sponsored by the non-profit Wikimedia Foundation. It contains entries both on traditional encyclopedic topics and on almanac, gazetteer, and current events topics. Its purpose is to create and distribute a free international encyclopedia in as many languages as possible. Wikipedia is the most popular reference site on the internet, receiving tens of millions of hits per day.
The English section of Wikipedia has over 2 million articles and is growing fast. It is edited by volunteers in wiki fashion, meaning articles are subject to change by nearly anyone. Wikipedia's volunteers enforce a policy of "neutral point of view" whereby views presented about notable persons or literature are summarized without an attempt to determine an objective truth. Because of its open nature, vandalism and inaccuracy are problems in Wikipedia.
The status of Wikipedia as a reference work has been controversial, and it is both praised for its free distribution, free editing and wide range of topics and criticized for alleged systemic biases, preference of consensus to credentials, deficiencies in some topics, and lack of accountability and authority when compared with traditional encyclopedias. Its articles have been cited by the mass media and academia and are available under the GNU Free Documentation License'''
wordlist = s.split()
print(wordlist)
pmf2 = Pmf()
for word in wordlist:
    pmf.Incr(word,1)
pmf.Normalize()
print(pmf.Prob('of'))