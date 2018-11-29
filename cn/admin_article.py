#-*- coding: utf-8 -*-
from flask import Blueprint,render_template,request,abort,redirect,url_for,session,flash
from article import Article
from board import Board,Forum,Catagory
import usermanage
import formvalidate
import articleselect
import json
import re
import os
import time
import hashlib
import urllib

admin_article=Blueprint("admin_article",__name__,template_folder="admin_templates")



@admin_article.route('/upload/',methods=['GET','POST'])
def upload():
    action = request.args.get('action')
    result=""
    # with open(os.path.join('/ueditor','php','config.json')) as fp:
    with open(os.path.join('ueditor','php','config.json')) as fp:
        try:
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        result = CONFIG


    if action in ('uploadimage', 'uploadvideo', 'uploadfile'):
        upfile = request.files['upfile']
        #use secure_filename is a secure function to get filename ranther than direct file.filename
        orignalName=upfile.filename
        filename=urllib.quote(orignalName.encode('utf-8'))
        preFilename=filename[:filename.rfind('.')]
        md5=hashlib.md5()
        md5.update(preFilename)
        preFilename=md5.hexdigest()
        postFix='.'+filename.split('.')[-1]
        newFileName='%s_%d%s'%(preFilename,time.time(),postFix)
        upfile.save(os.path.join('upload',newFileName))
        result={
            "state":"SUCCESS",
            "url":newFileName,
            "title":orignalName,
            "original":orignalName
        }

    return json.dumps(result)



@admin_article.route("/board/<int:board_id>")
@admin_article.route("/")
def list_articles(board_id=2):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	board=Board.getboard(board_id)
	if board==None:
		abort(404)
		
	try:
		catagory_id=int(request.args["catagory_id"])
	except (KeyError,ValueError) as e:
		catagory_id=None
	except (Exception) as e:
		abort(404)
	
	try:
		page_id=int(request.args["page_id"])
	except (KeyError,ValueError) as e:
		page_id=1
	except (Exception) as e:
		about(404)
	
	board=articleselect.select_by_catagory(board,catagory_id)
	board=articleselect.select_by_page(board,page_id)
	
	return render_template("admin_article.html",board=board,current_catagory_id=catagory_id,current_page_id=page_id)
	
@admin_article.route("/board/<int:board_id>/create",methods=["POST"])
def create_catagory(board_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	
	board=Board.getboard(board_id)
	if board==None:
		abort(404)
	
	catagory_form=formvalidate.Catagory_Form(request.form)
	
	if catagory_form.validate():
		if board.create_catagory(catagory_form.catagory_name.data):
			flash(u"成功创建了一个分类","success")
			return redirect(url_for("admin_article.list_articles",board_id=board.id))
		else:
			abort(500)
	else:
		flash(u"创建分类失败，请检查是否填写了分类名称","error")
		return redirect(url_for("admin_article.list_article",board_id=board.id))
		
@admin_article.route("/board/<int:board_id>/delete/<int:catagory_id>")
def delete_catagory(board_id,catagory_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	
	board=Board.getboard(board_id)
	if board==None:
		abort(404)
	
	if board.catagorys==None:
		abort(404)
	
	if board.articles==None:
		abort(404)
		
		
	try:
		catagory=board.catagorys[catagory_id]
	except (KeyError):
		abort(404)
		
	for article_id,article in board.articles.iteritems():
		if article.catagory!=None:
			if article.catagory.id==catagory.id:
				flash(u"你不能删除分类，如果该分类下还有文章的话","error")
				return redirect(url_for("admin_article.list_articles",board_id=board.id))
	
	if board.delete_catagory(catagory.id):
		flash(u"删除分类成功","success")
		return redirect(url_for("admin_article.list_articles",board_id=board.id))
	else:
		flash(u"你不能删除分类，如果该分类下还有文章的话","error")
		return redirect(url_for("admin_article.list_articles",board_id=board.id))
		
		
		
@admin_article.route("/board/<int:board_id>/article/<int:article_id>/changecatagory/<int:catagory_id>")
def change_article_catagory(board_id,article_id,catagory_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	
	board=Board.getboard(board_id)
	if board==None:
		abort(404)
		
	try:
		article=board.articles[article_id]
	except (KeyError):
		abort(404)
		
	try:
		catagory=board.catagorys[catagory_id]
	except (KeyError):
		abort(404)
		
	
	if board.move_article_to_catagory(article.id,catagory.id):
		return redirect(url_for("admin_article.list_articles",board_id=board.id))
	else:
		flash(u"变更分类失败","error")
		return redirect(url_for("admin_article.list_articles",board_id=board.id))

@admin_article.route("/board/<int:board_id>/article/<int:article_id>/removecatagory")
def remove_article_catagory(board_id,article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	
	board=Board.getboard(board_id)
	if board==None:
		abort(404)
		
	try:
		article=board.articles[article_id]
	except (KeyError):
		abort(404)
	
	if board.move_article_to_catagory(article.id,None):
		return redirect(url_for("admin_article.list_articles",board_id=board.id))
	else:
		flash(u"移除分类失败","error")
		return redirect(url_for("admin_article.list_articles",board_id=board.id))
	



@admin_article.route("/create",methods=["GET","POST"])
def create():
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
		
	articleform=formvalidate.ArticleForm_Create(request.form)
	
	all_forum=Forum.get_all_forum()
	
	articleform.forum.choices=[(forum_id,forum.name) for forum_id,forum in all_forum.iteritems()]
	if request.method=="GET":
		return render_template("admin_create_article.html",form=articleform)
	
	if request.method=="POST" and articleform.validate():
		article=Article(id=0,title=articleform.title.data,forum=all_forum[articleform.forum.data],abstract=articleform.abstract.data,content=articleform.content.data,source=articleform.source.data)
		if article.inserttodatabase():
			flash(u"添加文章成功","success")
			return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
		
	return render_template("admin_create_article.html",form=articleform)
	

@admin_article.route("/update/<int:article_id>",methods=["GET","POST"])
def update_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	if article==None:
		return abort(404)

	articleform=formvalidate.ArticleForm_Update(request.form,article)
	
	
	if request.method=="GET":
		return render_template("admin_update_article.html",form=articleform)
	
	if request.method=="POST" and articleform.validate():
		article.title=articleform.title.data
		article.abstract=articleform.abstract.data
		article.content=articleform.content.data
		article.source=articleform.source.data
		if article.updatetodatabase():
			flash(u"文章已经更新","success")
			return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	
	return render_template("admin_update_article.html",form=articleform)

@admin_article.route("/delete/<int:article_id>",methods=["GET","POST"])
def delete_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	if article==None:
		abort(404)
	
	if article.deletetodatabase():
		flash(u"文章已经删除","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"文章删除失败，如果持续出现这个问题请联系服务器管理员！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))



@admin_article.route("/recommend/<int:article_id>",methods=["GET","POST"])
def recommend_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	
	if article==None:
		return abort(404)
	
	if article.recommend():
		flash(u"文章已加入推荐列表","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"操作失败，如果持续出现这个问题请联系服务器管理员！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	
@admin_article.route("/unrecommend/<int:article_id>",methods=["GET","POST"])
def unrecommend_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	
	if article==None:
		return abort(404)
	
	if article.unrecommend():
		flash(u"文章已移除推荐列表","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"操作失败！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	
@admin_article.route("/bold/<int:article_id>",methods=["GET","POST"])
def bold_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	
	if article==None:
		return abort(404)
	
	if article.bold():
		flash(u"文章标题已加粗","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"操作失败！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))

@admin_article.route("/unbold/<int:article_id>",methods=["GET","POST"])
def unbold_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	
	if article==None:
		return abort(404)
	
	if article.unbold():
		flash(u"文章标题加粗已经取消","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"操作失败！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))

@admin_article.route("/stick/<int:article_id>",methods=["GET","POST"])
def stick_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	
	if article==None:
		return abort(404)
	
	if article.stick():
		flash(u"文章已经置顶","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"操作失败！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))

@admin_article.route("/unstick/<int:article_id>",methods=["GET","POST"])
def unstick_article(article_id):
	user=usermanage.check_login_state(session)
	if user==None:
		return redirect(url_for("admin_user.user_login"))
	article=Article.getarticle(article_id)
	
	if article==None:
		return abort(404)
	
	if article.unstick():
		flash(u"文章置顶已经取消","success")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))
	else:
		flash(u"操作失败！","error")
		return redirect(url_for("admin_article.list_articles",board_id=article.forum.id))

