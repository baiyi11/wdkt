import string
import random
from datetime  import datetime

def make_captcha(digit: int) ->str:
    """
    邮箱验证码工具

    :param digit:验证码位数
    
    :Return str: 验证码
    """
    letters=string.ascii_letters+string.digits
    captcha="".join(random.sample(letters,digit))
    return captcha


def  today() ->str:
    """
    获取当前日期
    """
    today=datetime.now().strftime("%Y-%m-%d")
    return today


