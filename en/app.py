# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,abort,redirect,url_for,g
from article import Article
import articleselect
from board import Board,Forum,Catagory
from admin_file import admin_file
from admin_article import admin_article
from admin_index import admin_index
from admin_user import admin_user
from admin_help import admin_help
#注册
from register import register
import index_setting


#popsite=Flask("polaroceanportal")
popsite=Flask("polaroceanportal",static_url_path='',static_folder='',static_path='')
# popsite=Flask(__name__,static_folder='',static_url_path='')
popsite.config["name"]=u"Polar and Ocean Portal"
popsite.config["chinese_name"]=u"国际极地与海洋门户"


popsite.secret_key="popsite_secret_key"
popsite.register_blueprint(admin_user,url_prefix="/admin/user")
popsite.register_blueprint(admin_file,url_prefix="/admin/file")
popsite.register_blueprint(admin_article,url_prefix="/admin/article")
popsite.register_blueprint(admin_index,url_prefix="/admin/index")
popsite.register_blueprint(admin_help,url_prefix="/admin/help")
#注册
popsite.register_blueprint(register,url_prefix="/admin/register")

@popsite.route("/")
@popsite.route("/index.html")
@popsite.route("/index")
def index():
	all_board={}
	for i in range(1,11):
		board=Board.getboard(i)
		all_board[board.id]=board
		
	all_board[12]=Board.getboard(12)
	all_board[13]=Board.getboard(13)
	all_board[14]=Board.getboard(14)
	all_board[15]=Board.getboard(15)
	
	jumbotron=index_setting.Jumbotron.getfromdatabase()
	professors=index_setting.professors
	scholars=index_setting.scholars
	professors.populate_items()
	scholars.populate_items()
	footer = index_setting.footerList
	footer.populate1_items()
	return render_template("index.html",all_board=all_board,jumbotron=jumbotron,professors=professors,scholars=scholars,footer=footer)
	
@popsite.route("/article/<int:article_id>")
def article(article_id):
	article=Article.getarticle(article_id)
	if article!=None:
		recommended=Forum.get_recommended_forum()
		lastest=Forum.get_lastest_news()
		footer = index_setting.footerList
		footer.populate1_items()
		return render_template("article.html",article=article,recommended=recommended,lastest=lastest,footer=footer)
	else:
		recommended=Forum.get_recommended_forum()
		lastest=Forum.get_lastest_news()
		footer = index_setting.footerList
		footer.populate1_items()
		return render_template("articlenotfount.html",recommended=recommended,lastest=lastest,footer=footer)
	
@popsite.route("/board/<int:board_id>")
def board(board_id):
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
		abort(404)
		
	

	board=Board.getboard(board_id)
	if board==None:
		abort(404)
	else:
		board=articleselect.select_by_catagory(board,catagory_id)
		board=articleselect.select_by_page(board,page_id)
		recommended=Forum.get_recommended_forum()
		lastest=Forum.get_lastest_news()
		footer = index_setting.footerList
		footer.populate1_items()
		return render_template("catalog.html",board=board,recommended=recommended,lastest=lastest,current_catagory_id=catagory_id,current_page_id=page_id,footer=footer)
	
@popsite.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
@popsite.errorhandler(500)
def server(error):
    return render_template('500.html'), 500
   
if __name__=="__main__":
    popsite.run(debug=True)
