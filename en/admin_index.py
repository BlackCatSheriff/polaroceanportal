# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, abort, redirect, url_for, session, flash
from article import Article
from board import Board, Forum, Catagory
import filemanage
import index_setting
import usermanage
import formvalidate

admin_index = Blueprint("admin_index", __name__, template_folder="admin_templates")


@admin_index.route("/jumbotron")
@admin_index.route("/")
def index_jumbotron():
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))
    jumbotron = index_setting.Jumbotron.getfromdatabase()

    jumbotron_form = formvalidate.Jumbotron_Form(request.form, jumbotron)

    if jumbotron == None:
        abort(500)

    return render_template("admin_index_jumbotron.html", jumbotron=jumbotron_form)


@admin_index.route("/jumbotron/update", methods=["POST"])
def update_jumbotron():
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))
    jumbotron = index_setting.Jumbotron.getfromdatabase()
    if jumbotron == None:
        abort(500)

    jumbotron_form = formvalidate.Jumbotron_Form(request.form, jumbotron)

    if jumbotron_form.validate():
        jumbotron.title = jumbotron_form.title.data
        jumbotron.content = jumbotron_form.content.data
        jumbotron.link = jumbotron_form.link.data
        jumbotron.image_link = jumbotron_form.image_link.data
        if jumbotron.updatetodatabase():
            flash(u"已经更新了巨幕", "success")
            return redirect(url_for("admin_index.index_jumbotron"))
        else:
            abort(500)
    else:
        flash(u"巨幕更新失败，请检查是否填写了巨幕标题和巨幕图片链接", "error")
        return render_template("admin_index_jumbotron.html", jumbotron=jumbotron_form)


@admin_index.route("/aboutus", methods=["GET", "POST"])
def set_aboutus_address():
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    aboutus = index_setting.Aboutus.get_from_database()
    if not aboutus:
        abort(500)

    aboutus_form = formvalidate.Aboutus_Form(request.form, aboutus)
    if request.method == "GET":
        return render_template("admin_index_aboutus.html", aboutus=aboutus_form)
    else:
        if aboutus_form.validate():
            aboutus.address = aboutus_form.address.data
            if aboutus.update_to_database():
                flash(u"关于我们链接地址更新成功", "success")
                return render_template("admin_index_aboutus.html", aboutus=aboutus_form)
            else:
                flash(u"关于我们链接地址更新失败", "error")
                return render_template("admin_index_aboutus.html", aboutus=aboutus_form)
        else:
            flash(u"更新失败，请检查是否正确填写了链接地址", "error")
            return render_template("admin_index_aboutus.html", aboutus=aboutus_form)


@admin_index.route("/footer")
@admin_index.route("/")
def index_footer():
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    footer = index_setting.footerList

    if footer.populate1_items():
        return render_template("admin_index_footer.html", footer=footer)
    else:
        abort(500)


@admin_index.route("/footer/create", methods=["GET", "POST"])
def add_footer_item():
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    footer = index_setting.footerList

    footer_item_form = formvalidate.Footer_Item_Form(request.form)
    footer_item_form.footer = footer

    if request.method == "GET":
        return render_template("admin_create_footer_item.html", item=footer_item_form)
    elif footer_item_form.validate():
        item = footer.create_item(footer_item_form.name.data, footer_item_form.link.data)
        if item:
            flash(u"已经添加了合作单位", "success")
            return redirect('/admin/index/footer')
        else:
            abort(500)
    else:
        flash(u"添加合作单位失败，请检查是否填写了合作单位的标题，链接，地址请保证HTTP协议开头", "error")
        return render_template("admin_create_footer_item.html", item=footer_item_form)


@admin_index.route("/footer/delete/<int:item_id>", methods=["GET", "POST"])
def delete_footer_item(item_id):
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    footer = index_setting.footerList

    item = footer.get_item(item_id)
    if item == None:
        abort(404)

    if item.delete():
        flash(u"已经删除了该项", "success")
        return redirect('/admin/index/footer')
    else:
        abort(500)


@admin_index.route("/footer/update/<int:item_id>", methods=["GET", "POST"])
def update_footer_item(item_id):
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    footer = index_setting.footerList

    item = footer.get_item(item_id)
    if item == None:
        abort(404)

    footer_item_form = formvalidate.Footer_Item_Form(request.form, item)
    footer_item_form.footer = footer

    if request.method == "GET":
        return render_template("admin_update_footer_item.html", item=footer_item_form)
    elif footer_item_form.validate():
        item.name = footer_item_form.name.data
        item.link = footer_item_form.link.data
        if item.update():
            flash(u"已经更新了合作单位", "success")
            footer=index_setting.footerList
            return redirect('/admin/index/footer')
        else:
            abort(500)
    else:
        flash(u"更新合作单位失败，请检查是否填写了标题，链接，地址请保证HTTP协议开头", "error")
        return render_template("admin_update_footer_item.html", item=footer_item_form)


@admin_index.route("/slick")
@admin_index.route("/slick/<slick_name>")
def index_slick(slick_name="scholars"):
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    if slick_name == "professors":
        slick = index_setting.professors
    elif slick_name == "scholars":
        slick = index_setting.scholars
    else:
        abort(404)

    if slick.populate_items():
        return render_template("admin_index_slick.html", slick=slick)
    else:
        abort(500)


@admin_index.route("/slick/<slick_name>/create", methods=["GET", "POST"])
def add_slick_item(slick_name):
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    if slick_name == "professors":
        slick = index_setting.professors
    elif slick_name == "scholars":
        slick = index_setting.scholars
    else:
        abort(404)

    slick_item_form = formvalidate.Slick_Item_Form(request.form)
    slick_item_form.slick = slick

    if request.method == "GET":
        return render_template("admin_create_slick_item.html", item=slick_item_form)
    elif slick_item_form.validate():
        item = slick.create_item(slick_item_form.name.data, slick_item_form.link.data, slick_item_form.image_link.data)
        if item:
            flash(u"已经添加了滚动图片单元", "success")
            return redirect(url_for("admin_index.index_slick", slick_name=slick_name))
        else:
            abort(500)
    else:
        flash(u"添加滚动图片单元失败，请检查是否填写了滚动图片单元的标题，链接，图片链接，地址请保证HTTP协议开头", "error")
        return render_template("admin_create_slick_item.html", item=slick_item_form)


@admin_index.route("/slick/<slick_name>/delete/<int:item_id>", methods=["GET", "POST"])
def delete_slick_item(slick_name, item_id):
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))
    if slick_name == "professors":
        slick = index_setting.professors
    elif slick_name == "scholars":
        slick = index_setting.scholars
    else:
        abort(404)

    item = slick.get_item(item_id)
    if item == None:
        abort(404)

    if item.delete():
        flash(u"已经删除了滚动图片单元", "success")
        return redirect(url_for("admin_index.index_slick", slick_name=slick_name))
    else:
        abort(500)


@admin_index.route("/slick/<slick_name>/update/<int:item_id>", methods=["GET", "POST"])
def update_slick_item(slick_name, item_id):
    user = usermanage.check_login_state(session)
    if user == None:
        return redirect(url_for("admin_user.user_login"))

    if slick_name == "professors":
        slick = index_setting.professors
    elif slick_name == "scholars":
        slick = index_setting.scholars
    else:
        abort(404)

    item = slick.get_item(item_id)
    if item == None:
        abort(404)

    slick_item_form = formvalidate.Slick_Item_Form(request.form, item)
    slick_item_form.slick = slick

    if request.method == "GET":
        return render_template("admin_update_slick_item.html", item=slick_item_form)
    elif slick_item_form.validate():
        item.name = slick_item_form.name.data
        item.link = slick_item_form.link.data
        item.image_link = slick_item_form.image_link.data
        if item.update():
            flash(u"已经更新了滚动图片单元", "success")
            return redirect(url_for("admin_index.index_slick", slick_name=slick_name))
        else:
            abort(500)
    else:
        flash(u"更新滚动图片单元失败，请检查是否填写了滚动图片的标题，链接和图片链接，地址请保证HTTP协议开头", "error")
        return render_template("admin_update_slick_item.html", item=slick_item_form)






