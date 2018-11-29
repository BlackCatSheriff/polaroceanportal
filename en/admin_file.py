#-*-coding: utf-8 -*-
from flask import Blueprint,render_template,request,abort,redirect,url_for,session,flash
from article import Article
from board import Board,Forum,Catagory
import filemanage
import usermanage
import formvalidate

admin_file=Blueprint("admin_file",__name__,template_folder="admin_templates")

@admin_file.route("/")
@admin_file.route("/<bucket_name>")
def list_directorys(bucket_name="image"):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	bucket=filemanage.Bucket.get_bucket(bucket_name)
	if bucket:
		return render_template("admin_directory.html",bucket=bucket)
	else:
		abort(404)


@admin_file.route("/<bucket_name>/<directory_name>/upload",methods=["POST"])
def upload_file(bucket_name,directory_name):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	bucket=filemanage.Bucket.get_bucket(bucket_name)
	if bucket==None:
		abort(404)
	
	directory=bucket.get_dir(directory_name)
	
	if directory==None:
		abort(404)
	
	file=request.files["file"]
	
	if file:
		if directory.create_file(file):
			flash(u"文件上传成功","success")
			return redirect(url_for("admin_file.list_files",bucket_name=bucket_name,directory_name=directory_name))
			
	flash(u"文件上传失败，请勿上传大于2M的文件。","error")
	return redirect(url_for("admin_file.list_files",bucket_name=bucket_name,directory_name=directory_name))
		

@admin_file.route("/<bucket_name>/create",methods=["POST"])
def create_directory(bucket_name):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	bucket=filemanage.Bucket.get_bucket(bucket_name)
	if bucket==None:
		abort(404)
		
	
	
	dir_create_form=formvalidate.Directory_Create_Form(request.form)
	if dir_create_form.validate() and bucket.get_dir(dir_create_form.dir_name.data)==None:
		if bucket.create_dir(dir_create_form.dir_name.data):
			flash(u"已经成功创建了文件夹","success")
			return redirect(url_for("admin_file.list_directorys",bucket_name=bucket_name))
	
	flash(u"文件夹创建失败，请检查文件夹是否已经存在，文件夹名陈是否填写。","error")
	return redirect(url_for("admin_file.list_directorys",bucket_name=bucket_name))
	
@admin_file.route("/<bucket_name>/delete/<directory_name>")
def delete_direcotry(bucket_name,directory_name):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	bucket=filemanage.Bucket.get_bucket(bucket_name)
	
	if bucket==None:
		abort(404)

	directory=bucket.get_dir(directory_name)
	
	if directory==None:
		abort(404)

	if directory.delete():
		flash(u"成功删除了目录","error")
		return redirect(url_for("admin_file.list_directorys",bucket_name=bucket_name))
	
	flash(u"删除目录失败","error")
	return redirect(url_for("admin_file.list_directorys",bucket_name=bucket_name))
	

@admin_file.route("/<bucket_name>/<directory_name>")
def list_files(bucket_name,directory_name):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	bucket=filemanage.Bucket.get_bucket(bucket_name)
	if bucket==None:
		abort(404)
		
	directory=bucket.get_dir(directory_name)
	if directory==None:
		abort(404)
	
	
	return render_template("admin_file.html",directory=directory)
	

	
@admin_file.route("/<bucket_name>/<directory_name>/delete/<file_name>")
def delete_file(bucket_name,directory_name,file_name):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	bucket=filemanage.Bucket.get_bucket(bucket_name)
	if bucket==None:
		abort(404)
	
	directory=bucket.get_dir(directory_name)
	if directory==None:
		abort(404)
	
	file=directory.get_file(file_name)
	if file==None:
		abort(404)
	
	if file.delete():
		flash(u"删除文件成功","error")
		return redirect(url_for("admin_file.list_files",bucket_name=bucket_name,directory_name=directory_name))
	
	flash(u"文件删除失败","error")
	return redirect(url_for("admin_file.list_files",bucket_name=bucket_name,directory_name=directory_name))
