""" 
配置表
"""

import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(basedir, os.getenv('LOG_DIR', 'logs'))

class BaseConfig():
    """基础配置"""
    # JSON_AS_ASCII
    JSON_AS_ASCII=False
    # flask-mail配置
    MAIL_SERVER ="smtp.qq.com"
    MAIL_PORT =465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "sat119@qq.com"
    MAIL_PASSWORD = "fupqpggcyisobjdd"
    MAIL_DEFAULT_SENDER = "sat119@qq.com"

    # session会话
    SECRET_KEY="ADADASDASFS@324564512"

    # 首页每页行数
    HOME_PAGE_PER_PAGE = 5
    
    # 日志
    LOG_LEVEL = logging.INFO
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class ProductionConfig(BaseConfig):
    """
    生产环境配置
    """

   # 数据库信息
    HOSTNAME="127.0.0.1"
    PORT="3306"
    DATABASE="wdkt"
    USERNAME="mysql"
    PASSWORD="123456"
    DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """ 
    开发环境配置
    """
    # 数据库信息
    HOSTNAME="127.0.0.1"
    PORT="3306"
    DATABASE="wdkt"
    USERNAME="mysql"
    PASSWORD="123456"
    DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False




config={
    "production":ProductionConfig,
    "development":DevelopmentConfig
}
