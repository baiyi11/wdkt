import string
import random
import datetime
from logging.handlers  import BaseRotatingHandler
import os

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
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    return today




class DayRotatingHandler(BaseRotatingHandler):
    def __init__(self, filename, mode, encoding=None, delay=False):
        self.date = datetime.date.today()
        self.suffix = "%Y-%m-%d.log"
        super(BaseRotatingHandler, self).__init__(filename, mode, encoding, delay)

    def shouldRollover(self, record):
        return self.date != datetime.date.today()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        new_log_file = os.path.join(os.path.split(self.baseFilename)[0], datetime.date.today().strftime(self.suffix))
        self.baseFilename = "{}".format(new_log_file)
        self._open()