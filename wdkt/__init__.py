from flask import Flask
from wdkt.settings import config
from wdkt.blueprints import qa_bp,user_bp
from wdkt.exts  import db,mail,migrate,moment,cors
from wdkt.utils import DayRotatingHandler

import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
from wdkt.settings import log_dir

def create_app(config_name :str=None):
    """工厂函数"""
    if config_name is None:
        config_name = "development"
    else:
        config_name=config_name

    app=Flask("wdkt")
    app.config.from_object(config[config_name])

    # 注册扩展插件
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)

    register_logging(app)
    
    return  app


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(qa_bp)
    app.register_blueprint(user_bp)


def register_extensions(app):
    """注册扩展插件"""
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app,db)
    cors.init_app(app,supports_credentials=True)
    
    
def register_logging(app):
    """日志"""
    app.logger.name = 'wdkt'
    log_level = app.config.get("LOG_LEVEL", logging.INFO)
    cls_handler = logging.StreamHandler()
    log_file = os.path.join(log_dir, datetime.date.today().strftime("%Y-%m-%d.log"))
    file_handler = DayRotatingHandler(log_file, mode="a", encoding="utf-8")

    logging.basicConfig(level=log_level,
                        format="%(asctime)s %(name)s "
                               "%(filename)s[%(lineno)d] %(funcName)s() %(levelname)s: %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        handlers=[cls_handler, file_handler])

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(os.path.join(log_dir, 'wdkt.log'),maxBytes=1024 * 1024 * 50, backupCount=5, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(name)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))

            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)