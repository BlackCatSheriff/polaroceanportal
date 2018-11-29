# -*- coding: utf-8 -*-
from wtforms import StringField,TextAreaField,IntegerField,SelectField,PasswordField
from wtforms import Form
from wtforms import validators

from board import Forum

class Footer_Item_Form(Form):
	id=IntegerField(u"id",default=0)
	name=StringField(u"name",[validators.InputRequired()])
	link=StringField(u"link",[validators.InputRequired(),validators.URL()])

class Register(Form):
	# id = IntegerField(u"id",default=0)
	usn =TextAreaField(u"usn",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	name = TextAreaField(u"name", [validators.optional()])
	pwd =PasswordField(u"pwd",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])

	email = TextAreaField(u"email",[validators.optional()])
	workplace = TextAreaField(u"workplace",[validators.optional()])
#有待改动
class ArticleForm_Update(Form):
	
	id=IntegerField(u"id",default=0)
	
	title=StringField(u"title",[validators.InputRequired(u"请输入文章标题")])
	
	abstract=TextAreaField(u"abstract",[validators.optional()])
	
	content=TextAreaField(u"content",[validators.optional()])
	
	source=StringField(u"source",[validators.optional()])
	
class ArticleForm_Create(ArticleForm_Update):

	forum=SelectField(u"forum",coerce=int)
	
	
class Catagory_Form(Form):
	
	catagory_name=StringField(u"catagory_name",[validators.InputRequired()])
	
	
class Directory_Create_Form(Form):
	dir_name=StringField(u"dir_name",[validators.InputRequired(u"请输入目录名称"),validators.regexp("^[a-z0-9A-Z_-]+$")])
	


class Jumbotron_Form(Form):
	title=StringField(u"title",[validators.InputRequired()])
	content=TextAreaField(u"content",[validators.optional()])
	link=StringField(u"link",[validators.optional(),validators.URL()])
	image_link=StringField(u"image_link",[validators.InputRequired()])
	
class Aboutus_Form(Form):
	address=StringField(u"address",[validators.InputRequired(),validators.URL()])
	
class Slick_Item_Form(Form):
	id=IntegerField(u"id",default=0)
	name=StringField(u"name",[validators.InputRequired()])
	link=StringField(u"link",[validators.InputRequired(),validators.URL()])
	image_link=StringField(u"image_link",[validators.InputRequired()])
	
class User_Login_Form(Form):
	name=StringField(u"name",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	passwd=PasswordField(u"passwd",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])

class Create_User_Form(Form):
	name=StringField(u"name",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	passwd=PasswordField(u"passwd",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	confirm=PasswordField(u"confirm",[validators.InputRequired(),validators.EqualTo("passwd")])
	
	
class Change_Passwd_Form(Form):
	#passwd=PasswordField(u"passwd",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	new_passwd=PasswordField(u"new_passwd",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	confirm=PasswordField(u"confirm",[validators.InputRequired(),validators.EqualTo("new_passwd")])
	
class Reset_Passwd_Form(Form):
	new_passwd=PasswordField(u"new_passwd",[validators.InputRequired(),validators.regexp("^[a-z0-9A-Z_-]{6,16}$")])
	confirm=PasswordField(u"confirm",[validators.InputRequired(),validators.EqualTo("new_passwd")])
