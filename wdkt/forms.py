'''
Description: 
Author: baiyi
Date: 2022-02-24 14:49:49
LastEditTime: 2022-04-02 15:07:13
LastEditors: baiyi
Reference: 
'''
from wdkt.models import EmailCaptchaModel,UserModel
import  wtforms
from wtforms.validators import email,length,EqualTo

class RegisterForm(wtforms.Form):
    """
    注册表单验证
    """

    username=wtforms.StringField(validators=[length(min=1,max=20)])
    password=wtforms.StringField(validators=[length(min=3,max=20)])
    re_password=wtforms.StringField(validators=[EqualTo("password")])
    email=wtforms.StringField(validators=[email()])
    captcha=wtforms.StringField(validators=[length(min=4,max=4)])

    def validate_captcha(self,field):
        """
        检查验证码是否有效
        """

        captcha=field.data
        email=self.email.data
        captcha_model=EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower()!=captcha.lower():
            raise wtforms.ValidationError("验证码错误")

    def validate_email(self,field):
        """
        验证邮箱是否已经注册
        """
        
        email=field.data
        user_model=UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱已经注册")



class LoginForm(wtforms.Form):
    """
    登陆表单验证
    """
    email=wtforms.StringField(validators=[email()])
    password=wtforms.StringField(validators=[length(min=3,max=20)])


class QaForm(wtforms.Form):
    """
    发布问答验证
    """
    title=wtforms.StringField(validators=[length(min=1,max=2000)])
    content=wtforms.StringField(validators=[length(min=6,max=2000)])     

class CommentForm(wtforms.Form):
    """
    评论验证
    """
    content=wtforms.StringField(validators=[length(min=6,max=2000)])
    