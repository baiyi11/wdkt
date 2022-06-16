from wdkt.exts import db
from sqlalchemy import  Column ,BigInteger, Integer,Text,String,DateTime,Date

class EmailCaptchaModel(db.Model):
    """邮箱验证码模型"""
    __tablename__ = 'email_captcha'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    email=Column(String(100),nullable=False,unique=True,comment='邮件')
    captcha=Column(String(10),nullable=False,comment='验证码')
    create_time=Column(DateTime,comment='创建日期')


class UserModel(db.Model):
    """用户模型"""
    __tablename__='user'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    username=Column(String(200),nullable=False,unique=True,comment='用户名')
    email=Column(String(200),nullable=False,unique=True,comment='邮件')
    password=Column(String(200),nullable=False,comment='密码')
    create_time=Column(DateTime,nullable=False,comment='创建日期')
    is_deleted=Column(Integer(),default=0,comment='是否删除')


class QaModel(db.Model):
    """提问模型"""
    __tablename__='question'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    user_id=Column(BigInteger(),nullable=False,comment='用户ID')
    title=Column(String(200),nullable=False,comment='标题')
    content=Column(Text,nullable=False,comment='内容')
    create_time=Column(DateTime,comment='创建日期')
    is_deleted=Column(Integer(),default=0,comment='是否删除')
    category=Column(String(2000),comment='文章分类')


class CommentModel(db.Model):
    """评论模型"""
    __tablename__ = 'comment'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    user_id=Column(BigInteger(),nullable=False,comment='用户ID')
    question_id=Column(BigInteger(),nullable=False,comment='问题ID')
    content=Column(Text,nullable=False,comment='内容')
    create_time=Column(DateTime,comment='创建日期')
    # p_id=Column(BigInteger(),comment="回复评论ID")
    is_deleted=Column(Integer(),default=0,comment='是否删除')

class CommentUpModel(db.Model):
    """提问点赞模型"""
    __tablename__ = 'comment_up'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    user_id=Column(BigInteger(),nullable=False,comment='用户ID')
    question_id=Column(BigInteger(),nullable=False,comment='问题ID')
    is_deleted=Column(Integer(),default=0,comment='是否删除')


class CategoryModel(db.Model):
    """文章分类模型"""
    __tablename__ = 'category'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    create_time=Column(DateTime,comment='创建日期')


class QaPvModel(db.Model):
    """问题浏览量"""
    __tablename__ = 'question_pv'
    id=Column(BigInteger(), primary_key=True,autoincrement=True)
    browse_date=Column(Date,comment='浏览日期')
    question_id=Column(BigInteger(),nullable=False,comment='问题ID')
    pv=Column(BigInteger(),nullable=False,comment='PV')