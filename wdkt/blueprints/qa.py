'''
Description: 
Author: baiyi
Date: 2022-02-22 16:06:51
LastEditTime: 2022-04-02 21:26:36
LastEditors: baiyi
Reference: 
'''


from flask import Blueprint, render_template, session, url_for, redirect, request, g, flash, jsonify, current_app
from wdkt.decorators import login_required
from wdkt.models import QaModel, UserModel, CommentModel
from wdkt.forms import QaForm, CommentForm
from datetime import datetime
from wdkt.exts import db
from sqlalchemy import or_, func


bp = Blueprint("qa", __name__)


class Question():
    def __init__(self, id, content, create_time, title, username, comment_cnt) -> None:
        self.id = id
        self.content = content
        self.create_time = create_time
        self.title = title
        self.username = username
        self.comment_cnt = comment_cnt


@bp.route("/", defaults={"page": 1})
@bp.route("/page/<int:page>")
def index(page):
    """首页"""

    search_keyword = request.args.get("search")

    # 分页每页行数
    per_page = current_app.config["HOME_PAGE_PER_PAGE"]

    if not search_keyword:
        # 分页对象
        pagination = db.session \
            .query(QaModel.content, QaModel.create_time, QaModel.title, UserModel.username, QaModel.id) \
            .join(UserModel, QaModel.user_id == UserModel.id) \
            .order_by(QaModel.create_time.desc()) \
            .paginate(page, per_page=per_page, error_out=False)

    else:
        pagination = db.session \
            .query(QaModel.content, QaModel.create_time, QaModel.title, UserModel.username, QaModel.id) \
            .join(UserModel, QaModel.user_id == UserModel.id) \
            .filter(or_(QaModel.content.contains(search_keyword), QaModel.title.contains(search_keyword))) \
            .order_by(QaModel.create_time.desc()) \
            .paginate(page, per_page=per_page, error_out=False)

    # 当前页数据
    questions = pagination.items

    # 文章id
    question_ids = [question.id for question in questions]
    # 评论数
    comment_analysis = db.session \
        .query(CommentModel.question_id, func.count(CommentModel.id).label("comment_cnt")) \
        .filter(CommentModel.question_id.in_(question_ids))  \
        .group_by(CommentModel.question_id)   \
        .all()

    # 左连接取评论数
    new_questions = []
    for question in questions:
        i_index = []
        for i in comment_analysis:
            i_index.append(i.question_id)
            if question.id == i.question_id:
                new_questions.append(Question(id=question.id,
                                              content=question.content,
                                              create_time=question.create_time,
                                              title=question.title,
                                              username=question.username,
                                              comment_cnt=i.comment_cnt
                                              ))
        if question.id not in i_index:
            new_questions.append(Question(id=question.id,
                                          content=question.content,
                                          create_time=question.create_time,
                                          title=question.title,
                                          username=question.username,
                                          comment_cnt=0
                                          ))

    if questions:
        return render_template("index.html", questions=new_questions, pagination=pagination, search_keyword=search_keyword)
    else:
        return render_template("404.html")


@bp.route("/qa", methods=["GET", "POST"])
@login_required
def post_qa():
    """发布问答页面"""

    if request.method == "GET":
        return render_template("qa.html")
    else:
        forms = QaForm(request.form)
        if forms.validate():
            title = forms.title.data
            content = forms.content.data
            create_time = datetime.now()
            user = g.get("user")
            question = QaModel(user_id=user.id, content=content,
                               create_time=create_time, title=title)
            db.session.add(question)
            db.session.commit()

            return redirect('/')

        else:
            flash("标题或者内容不符合格式要求")
            return redirect(url_for("qa.post_qa"))


@bp.route("/detail/<int:question_id>")
def question_detail(question_id):
    """详情页面"""

    question = db.session \
        .query(QaModel.content, QaModel.create_time, QaModel.title, UserModel.username, QaModel.id) \
        .join(UserModel, QaModel.user_id == UserModel.id) \
        .filter(QaModel.id == question_id) \
        .first()

    comments = db.session \
        .query(CommentModel.id, CommentModel.create_time, CommentModel.content, UserModel.username) \
        .join(UserModel, CommentModel.user_id == UserModel.id)  \
        .filter(CommentModel.question_id == question_id) \
        .order_by(CommentModel.create_time.desc())  \
        .all()

    return render_template("detail.html", question=question, comments=comments)


@bp.route("/comment/<int:question_id>", methods=["POST"])
@login_required
def comment(question_id):
    """评论"""

    if request.method == "POST":
        forms = CommentForm(request.form)
        if forms.validate():
            content = forms.content.data
            user = g.get("user")
            create_time = datetime.now()
            comment_model = CommentModel(
                content=content, user_id=user.id, question_id=question_id, create_time=create_time)
            db.session.add(comment_model)
            db.session.commit()
            return redirect(url_for("qa.question_detail", question_id=question_id))
        else:
            flash("评论内容长度小于6个字符")
            return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():

    return render_template("base copy.html")
