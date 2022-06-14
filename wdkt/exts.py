'''
Description: 
Author: baiyi
Date: 2022-02-22 15:49:06
LastEditTime: 2022-02-23 14:00:52
LastEditors: baiyi
Reference: 
'''
from flask_sqlalchemy import  SQLAlchemy
from flask_mail import Mail
from flask_migrate  import  Migrate

db=SQLAlchemy()
mail=Mail()
migrate=Migrate()
