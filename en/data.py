# -*- coding: utf-8 -*-
import datetime
import articleselect
import sqlite3
import collections

DatabasePath="database"




class Forum(object):
	def __init__(self,id,name):
		"""可以是临时板块"""
		self.id=id
		self.name=name
		
class Board(Forum):
	def __init__(self,id,name,catagorys=None,articles=None):
		"""构造一个板块需要所有的catagory和article"""
		self.id=id
		self.name=name
		self.catagorys=catagorys
		self.articles=articles
	
	@staticmethod
	def getboard(id):
		"""从数据库中获取一整个板块"""
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		try:
			c.execute("\
select \
	article.id as article_id, \
	article.time as article_time, \
	article.title as article_title, \
	article.abstract as article_abstract, \
	article.content as article_content, \
	article.source as article_source, \
	article.source_link as article_source_link, \
	article.title_bold as article_title_bold, \
	forum.id as forum_id, \
	forum.name as forum_name, \
	catagory.id as catagory_id, \
	catagory.name as catagory_name \
from \
	forum inner join article on \
		forum.id=article.forum_id \
	left join catagory on \
		article.catagory_id=catagory.id and catagory.forum_id=forum.id \
where \
	forum.id=? order by article.id desc,catagory.id desc; \
",(id,))
		except (sqlite3.DatabaseError) as e:
			print e
			return None
		else:
			rows=c.fetchall()
		finally:
			conn.close()
			
		if rows==None:
			return None #forum不存在或者forum没有文章
		
		catagorys=collections.OrderedDict()
		articles=collections.OrderedDict()
		board=Board(id,"Currently Unset",catagorys,articles)
		for row in rows:
			article_id=row["article_id"]
			article_time=row["article_time"]
			article_title=row["article_title"]
			article_abstract=row["article_abstract"]
			article_content=row["article_content"]
			article_source=row["article_source"]
			article_source_link=row["article_source_link"]
			article_title_bold=row["article_title_bold"]
			forum_id=row["forum_id"]
			forum_name=row["forum_name"]
			catagory_id=row["catagory_id"]
			catagory_name=row["catagory_name"]
			
			board.name=forum_name
			
			if catagory_id!=None:
				try:
					catagory=catagorys[catagory_id]
				except (KeyError):
					catagory=Catagory(catagory_id,catagory_name,board)
					catagorys[catagory_id]=catagory
			else:
				catagory=None
				
			article_title_bold=(article_title_bold==1 and True) or False
			
			article=Article(id=article_id,title=article_title,forum=board,time=article_time,abstract=article_abstract,content=article_content,source=article_source,source_link=article_source_link,title_bold=article_title_bold,catagory=catagory)
			
			articles[article_id]=article
			
		if len(board.catagorys)==0:
			board.catagorys=None
		
		if len(board.articles)==0:
			board.articles=None
			
		return board
			
			
			
			
		

class Article(object):
	def __init__(self,id,title,forum,time=unicode(datetime.date.today()),abstract=None,content=None,source=None,source_link=None,title_bold=False,catagory=None):
	
		self.id=id
		self.title=title
		self.time=time
		self.forum=forum
		self.abstract=abstract
		self.content=content
		self.source=source
		self.source_link=source_link
		self.title_bold=title_bold
		self.catagory=catagory
	
	def __unicode__(self):
		result=u"id:"+unicode(self.id)+u";\ntitle:"+unicode(self.title)+u";\nforum_name:"+unicode(self.forum.name)+u";\nforum_id:"+unicode(self.forum.id)+u";\ntime:"+self.time+u";\nabstract:"+unicode(self.abstract)+u";\nsource:"+unicode(self.source)+u";\ncontent:"+unicode(self.content)
		return result
		
	def inserttodatabase(self):
		conn=sqlite3.connect(DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		
		try:
			c.execute("\
insert into article (title,time,abstract,content,source,forum_id,catagory_id) values (?,?,?,?,?,?,?)",\
(self.title,self.time,self.abstract,self.content,self.source,self.forum.id,None))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
			
		
	def updatetodatabase(self):
		conn=sqlite3.connect(DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		
		try:
			c.execute("\
update article set title=?,abstract=?,content=?,source=?,forum_id=?,catagory_id=? where id=?;",\
(self.title,self.abstract,self.content,self.source,self.forum.id,None,self.id))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
		
	@staticmethod
	def getarticle(id):
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
select \
	article.id as article_id, \
	article.time as article_time, \
	article.title as article_title, \
	article.abstract as article_abstract, \
	article.content as article_content, \
	article.source as article_source, \
	article.source_link as article_source_link, \
	article.title_bold as article_title_bold, \
	forum.id as forum_id, \
	forum.name as forum_name, \
	catagory.id as catagory_id,\
	catagory.name as catagory_name  \
from \
	article inner join forum on \
		forum.id=article.forum_id \
	left join catagory on \
		catagory.id=article.catagory_id and catagory.forum_id=forum.id \
where article.id=? \
",
(id,)
)
		except (sqlite3.DatabaseError) as e:
			print e
			return None
		else:
			row=c.fetchone()
		finally:
			conn.close()
		
		if row==None: #文章不存在
			return None
		
		
		tempforum=Forum(row["forum_id"],row["forum_name"])
		
		if row["catagory_id"]!=None:
			tempcatagory=Catagory(row["catagory_id"],row["catagory_name"],tempforum)
		else:
			tempcatagory=None  #没有catagory
			
		article_title_bold=(row["article_title_bold"]==1 and True) or False
		
		result=Article(id=row["article_id"],time=row["article_time"],title=row["article_title"],forum=tempforum,abstract=row["article_abstract"],content=row["article_content"],source=row["article_source"],source_link=row["article_source_link"],title_bold=row["article_title_bold"],catagory=tempcatagory)
		
		return result
	

	
class Catagory(object):
	def __init__(self,id,name,forum):
		self.id=id
		self.forum=forum
		self.name=name


def test():
	"""测试用的方法"""
	conn=sqlite3.connect(DatabasePath)
	c=conn.execute("select * from article inner join forum on forum.id=article.forum_id where article.id=?",(1,))
	return c

