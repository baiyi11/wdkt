from flask import Flask
from wdkt.settings import config
from wdkt.blueprints import qa_bp,user_bp
from wdkt.exts  import db,mail,migrate


def create_app(config_name=None) ->Flask:
    """工厂函数"""
    if config_name is None:
        config_name = config["development"]

    app=Flask("wdkt")

    app.config.from_object(config[config_name])


    # 注册扩展插件
    register_extensions(app)

    # 注册蓝图
    register_blueprints(app)

    return  app


def register_blueprints(app) ->None:
    """注册蓝图"""
    app.register_blueprint(qa_bp)
    app.register_blueprint(user_bp)


def register_extensions(app) ->None:
    """注册扩展插件"""
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
