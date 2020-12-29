#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 15:41
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# -*- coding: utf-8 -*-
# Author: YuZhiYi
# FILENAME : read_img.py
# TIME     : 2019/2/19 16:50
# pip install baidu-aip
from aip import AipOcr
from pprint import pprint
import time
""" 你的 APPID AK SK """
APP_ID = 'xxxxxxxx'
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()



""" 调用通用文字识别（高精度版） """
#ret = client.basicAccurate(images);

# """ 如果有可选参数 """
options = {}
options["detect_direction"] = "true"
options["probability"] = "true"


#pprint(ret)
# for i in range(1,8):
#     filePath = 'images\\' + str(i) + '.jpg'
#     images = get_file_content(filePath)
#     # """ 带参数调用通用文字识别（高精度版） """
#     ret = client.basicAccurate(images, options)
#     for row in ret[ 'words_result']:
#         print(row['words'])
#     time.sleep(1)

filePath = 'images\\image.jpg'
image = get_file_content(filePath)
# """ 带参数调用通用文字识别（高精度版） """
ret = client.basicAccurate(image, options)
for row in ret[ 'words_result']:
    print(row['words'])
time.sleep(1)