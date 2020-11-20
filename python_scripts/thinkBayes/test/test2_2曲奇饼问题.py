#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 17:07
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# 曲奇饼问题
# 在贝叶斯定理的语境下，可以很自然地使用一个Pmf映射每个假设对应的概率
# 在曲奇饼问题里面，应假设是B1和B2
from python_scripts.thinkBayes.code.thinkbayes import Pmf
pmf = Pmf()
pmf.Set('Bowl1',0.5)
pmf.Set('Bowl2',0.5)  # 这一分布包含了对每个假设的先验概率，成为先验分布

# 要更新基于新数据（拿到一块香草曲奇饼）后的分布，我们将先验分别乘以对应的似然度
pmf.Mult('Bowl1',0.75) #从碗1拿到的香草曲奇饼的可能性是3/4
pmf.Mult('Bowl2',0.5)  #从碗2拿到的香草曲奇饼的可能性是1/2

#如你所愿，Mult将给定假设的概率乘以已知的似然度
#更新后的分布还没有归一化，但由于这些假设互斥且构成了完全集合（意味着完全包含了所有可能假设）
#我们可以进行重新归一化
pmf.Normalize()  # 归一化

#其结果是一个包含每个假设的后验概率分布，这就是所说的后验分布

#最后可以得到假设碗1的后验概率分布
print(pmf.Prob('Bowl1'))
print(pmf.Prob('Bowl2'))