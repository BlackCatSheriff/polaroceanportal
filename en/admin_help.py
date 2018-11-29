#-*- coding: utf-8 -*-
from flask import Blueprint,render_template,request,abort,redirect,url_for,session,flash
import usermanage

admin_help=Blueprint("admin_help",__name__,template_folder="admin_templates")

@admin_help.route("/")
def help():
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	return render_template("admin_help.html")
