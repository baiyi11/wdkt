from flask import Flask
from wdkt.settings import config
from wdkt.blueprints import qa_bp,user_bp
from wdkt.exts  import db,mail,migrate,moment,cors

def create_app(config_name=None):
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