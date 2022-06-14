'''
Description: 
Author: baiyi
Date: 2022-02-22 16:06:41
LastEditTime: 2022-03-30 16:49:06
LastEditors: baiyi
Reference: 
'''

from datetime import datetime
from flask import  Blueprint,render_template,request,redirect,url_for,jsonify,session,flash
from wdkt.exts import mail,db
from flask_mail import Message
from wdkt.models import EmailCaptchaModel,UserModel
from wdkt.utils import  make_captcha
from wdkt.forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash

bp=Blueprint("user",__name__,url_prefix="/user")

@bp.route("/login" ,methods=["POST","GET"])
def login():
    """用户登录"""

    if request.method=="POST":
        forms=LoginForm(request.form)
        if forms.validate():

            email=forms.email.data
            password=forms.password.data
            # 哈希加密密码
            hash_password=generate_password_hash(password)
            user=UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password,password):
                session["user_id"]=user.id
                return redirect("/")
            else:
                flash("邮箱或者密码错误")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱或者密码格式错误")
            return redirect(url_for("user.login"))
    else:
        return render_template("login.html")


@bp.route("/logout")
def logout():
    """"用户注销"""

    # 清除session
    session.clear()
    return redirect(url_for("user.login"))
    


@bp.route("/regist",methods=['GET','POST'])
def regist():
    """用户注册"""

    if request.method=="GET":
        return render_template("regist.html")
    else:
    
        forms=RegisterForm(request.form)
        if forms.validate():
            
            password=forms.password.data
            email=forms.email.data
            username=forms.username.data
            # 哈希加密密码
            hash_password=generate_password_hash(password)

            user=UserModel(email=email,username=username,password=hash_password,create_time=datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
            
        else:
            print("验证未通过")
            return redirect(url_for("user.regist"))

@bp.route("/emailCaptcha",methods=['POST'])
def email_captcha():
    """ 发送验证码"""
    
    email=request.form.get("email")
    captcha=make_captcha(4)
    if mail:
        message=Message(
            subject="问答课堂验证码",
            recipients=[email],
            body=f"【问答课堂】你的注册验证码：{captcha},有效期5分钟,请不要泄露给他人。"
        )
        mail.send(message)
        captcha_model=EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha=captcha
            captcha_model.create_time=datetime.now()
            db.session.commit()
        else:
            captcha_model=EmailCaptchaModel(email=email,captcha=captcha,create_time=datetime.now())
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code":200})
    else:
        return jsonify({"code":400,"message":"请先传递邮箱"})
    
@bp.route("/edit")
def edit():
    """个人设置"""
    pass

@bp.route("/uploadavatar")
def upload_avatar():
    """上传头像"""
    pass

