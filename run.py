from wdkt import  create_app
from flask import session,g
from wdkt.models import UserModel

app=create_app(config_name="production")

@app.before_request
def get_userid():
    """"钩子函数,每个视图函数执行之前获取session里的user_id"""
    
    user_id=session.get("user_id")
    if user_id:
        try:
            user=UserModel.query.filter_by(id=user_id).first()
            #给g绑定一个叫做user的变量，它的值是user这个变量
            setattr(g,"user",user)
        except:
            g.user=None

@app.context_processor
def context_processor():
    """上下处理器"""
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)