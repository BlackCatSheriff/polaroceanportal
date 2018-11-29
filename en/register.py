#-*- coding: utf-8 -*-
from flask import Blueprint,render_template,request,abort,redirect,url_for,session,flash
from article import Article
from board import Board,Forum,Catagory
import filemanage
import usermanage
import formvalidate
import register_create
import index_setting



register = Blueprint("register", __name__, template_folder="admin_templates")

@register.route("/", methods=["GET","POST"])
def index():
    footer = index_setting.footerList
    footer.populate1_items()

    registers = register_create
    registeruser = formvalidate.Register(request.form)
    if request.method == "GET":
        return render_template("register.html", form = registeruser,footer = footer)
    elif registeruser.validate():
        if registers.createuser(registeruser.usn.data, registeruser.pwd.data,registeruser.name.data
                               ,registeruser.email.data, registeruser.workplace.data):
            flash(u"创建用户成功", "success")


            return render_template("register.html", form=registeruser,footer = footer)
        else:
            flash(u"创建用户失败，该用户名已被使用", "error")
            return render_template("register.html", form=registeruser,footer = footer)
    else:
        flash(u"创建用户失败，请检查用户名密码邮箱是否符合要求（6-16位仅限英文字母、数字、[-_]", "error")
        return render_template("register.html",form=registeruser,footer = footer)
