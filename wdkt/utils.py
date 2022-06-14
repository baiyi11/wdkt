'''
Description: 
Author: baiyi
Date: 2022-02-23 17:17:57
LastEditTime: 2022-02-24 10:10:02
LastEditors: baiyi
Reference: 
'''
import string
import random

def make_captcha(digit: int):
    """
    邮箱验证码工具

    :param digit:验证码位数
    
    :Return str: 验证码
    """
    letters=string.ascii_letters+string.digits
    captcha="".join(random.sample(letters,digit))
    return captcha

