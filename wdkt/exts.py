from flask_sqlalchemy import  SQLAlchemy
from flask_mail import Mail
from flask_migrate  import  Migrate
from flask_moment import  Moment
from flask_cors import CORS

db=SQLAlchemy()
mail=Mail()
migrate=Migrate()
moment=Moment()
cors=CORS()