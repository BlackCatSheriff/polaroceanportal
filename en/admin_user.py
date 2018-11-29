#-*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,abort,redirect,url_for,session,flash
import usermanage

import formvalidate

admin_user=Blueprint("admin_user",__name__,template_folder="admin_templates")

@admin_user.route("/")
@admin_user.route("/list")
def user_admin():
	
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	
	if user.name=="Administrator":
		all_user=user.get_all_user()
		if all_user==False:
			abort(500)
		return render_template("admin_user.html",user=user,all_user=all_user)
	else:
		return redirect(url_for("admin_user.change_passwd"))
	
	
	
@admin_user.route("/login",methods=["GET","POST"])
def user_login():
	user_login_form=formvalidate.User_Login_Form(request.form)
	if request.method=="GET":
		return render_template("admin_login.html",user=user_login_form)

	elif request.method=="POST" and user_login_form.validate():
		result=usermanage.login_user(session,user_login_form.name.data,user_login_form.passwd.data)
		if result:
			return redirect(url_for("admin_article.list_articles"))
		else:
			flash(u"用户名密码错误","error")
			return render_template("admin_login.html",user=user_login_form)
	else:
		flash(u"用户名密码格式错误","error")
		return render_template("admin_login.html",user=user_login_form)
		
		
		
	
@admin_user.route("/logout",methods=["GET"])
def user_logout():
	usermanage.logout_user(session)
	return redirect(url_for("admin_user.user_login"))
	
@admin_user.route("/delete/<user_name>")
def delete_user(user_name):
	
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	if user.name!="Administrator":
		return redirect(url_for("admin_user.change_passwd",user_name=user.name))
	
	if user.delete_user(user_name):
		flash(u"删除用户成功","success")
		return redirect(url_for("admin_user.user_admin"))
	else:
		abort(500)
	

@admin_user.route("/resetpasswd/<user_name>",methods=["GET","POST"])
def reset_user_passwd(user_name):
	
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	if user.name!="Administrator":
		return redirect(url_for("admin_user.change_passwd",user_name=user.name))
		
	if user.reset_passwd(user_name,user_name):
		flash(u"重置密码成功，重置后的密码与用户名相同，请联系用户立即修改密码。","success")
		return redirect(url_for("admin_user.user_admin"))
	else:
		abort(500)
	
@admin_user.route("/create",methods=["GET","POST"])
def create_user():
	
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	if user.name!="Administrator":
		return redirect(url_for("admin_user.change_passwd",user_name=user.name))
	
	create_user_form=formvalidate.Create_User_Form(request.form)
	if request.method=="GET":
		return render_template("admin_create_user.html",user=user,new_user=create_user_form)
	elif create_user_form.validate():
		if user.create_user(create_user_form.name.data,create_user_form.passwd.data):
			flash(u"创建用户成功","success")
			return redirect(url_for("admin_user.user_admin"))
		else:
			abort(500)
	else:
		flash(u"创建用户失败，请检查用户名密码是否符合要求（6-16位仅限英文字母、数字、[-_]","error")
		return render_template("admin_create_user.html",user=user,new_user=create_user_form)
		
	
@admin_user.route("/changepasswd",methods=["GET","POST"])
def change_passwd():
	
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	change_passwd_form=formvalidate.Change_Passwd_Form(request.form,user)
	
	if request.method=="GET":
		return render_template("admin_change_user_passwd.html",user=user,new_passwd_form=change_passwd_form)

	if change_passwd_form.validate():
		if user.change_passwd(change_passwd_form.new_passwd.data):
			flash(u"修改密码成功","success")
			return redirect(url_for("admin_article.list_articles"))
		else:
			flash(u"修改密码失败，请检查新密码是否符合格式要求（6-16位仅限英文字母、数字、[-_]","error")
			return render_template("admin_change_user_passwd.html",user=user,new_passwd_form=change_passwd_form)
	else:
		flash(u"修改密码失败，请检查新密码是否符合格式要求（6-16位仅限英文字母、数字、[-_]","error")
		return render_template("admin_change_user_passwd.html",user=user,new_passwd_form=change_passwd_form)
	
	
