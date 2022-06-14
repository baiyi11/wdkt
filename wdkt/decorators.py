'''
Description: 
Author: baiyi
Date: 2022-03-01 15:38:34
LastEditTime: 2022-03-30 13:17:27
LastEditors: baiyi
Reference: 
'''
from flask  import g,redirect,url_for
from functools import wraps

def login_required(func):
    """判断是否登录装饰器,已登录继续操作,未登录重定向登录页面"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g,"user"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.login"))
            
    return wrapper

