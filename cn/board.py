# -*- coding: utf-8 -*-

import sqlite3
import collections
import article
DatabasePath="database"


class Forum(object):
	def __init__(self,id,name):
		"""可以是临时板块"""
		self.id=id
		self.name=name
		
	@staticmethod
	def get_recommended_forum():
		recommended_forum=Forum(13,u"文章推荐")
	
		recommended_forum.articles=collections.OrderedDict()
	
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
	quicklinks.id as quicklinks_id \
from \
	quicklinks inner join article on \
		quicklinks.article_id=article.id \
order by \
	quicklinks.id desc; \
")
		except (sqlite3.DatabaseError) as e:
			print e
			recommended_forum.articles=None
			return recommended_forum
		else:
			rows=c.fetchall()
			for row in rows:
				article_id=row["article_id"]
				article_title=row["article_title"]
				article_time=row["article_time"]
				onearticle=article.Article(article_id,article_title,forum=recommended_forum,time=article_time)
				recommended_forum.articles[onearticle.id]=onearticle
				
			if len(recommended_forum.articles)==0:
				recommended_forum.articles=None
				
			return recommended_forum
		finally:
			conn.close()
		
	@staticmethod
	def get_all_forum():
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		try:
			c.execute(" \
select \
	id as forum_id ,\
	name as forum_name \
from board \
	order by id asc;")
		except (sqlite3.DatabaseError) as e:
			print e
			return None
		else:
			forum_rows=c.fetchall()
			result=collections.OrderedDict()
			for forum_row in forum_rows:
				one_forum=Forum(forum_row["forum_id"],forum_row["forum_name"])
				result[one_forum.id]=one_forum
			
			if len(result)==0:
				result=None
			
			return result
		finally:
			conn.close()
	
	@staticmethod
	def get_lastest_news():
		
		lastest_news_forum=Forum(14,u"最新新闻")
	
		lastest_news_forum.articles=collections.OrderedDict()
	
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		try:
			c.execute("\
select \
	article.id as article_id, \
	article.time as article_time, \
	article.title as article_title \
from \
	article \
where \
	article.board_id=2 \
order by \
	article.id desc \
limit 6; \
")
		except (sqlite3.DatabaseError) as e:
			print e
			lastest_news_forum.articles=None
			return lastest_news_forum
		else:
			article_rows=c.fetchall()
			for article_row in article_rows:
				article_id=article_row["article_id"]
				article_title=article_row["article_title"]
				article_time=article_row["article_time"]
				onearticle=article.Article(article_id,article_title,forum=lastest_news_forum,time=article_time)
				lastest_news_forum.articles[onearticle.id]=onearticle
			
			if len(lastest_news_forum.articles)==0:
				lastest_news_forum.articles=None
			
			return lastest_news_forum
			
		finally:
			conn.close()
			


		
		
class Catagory(object):
	def __init__(self,id,name,forum):
		self.id=id
		self.forum=forum
		self.name=name
	
	


		
class Board(Forum):
	def __init__(self,id,name,catagorys=None,articles=None):
		"""构造一个板块需要所有的catagory和article"""
		self.id=id
		self.name=name
		self.catagorys=catagorys
		self.articles=articles
		
		
	def create_catagory(self,catagory_name):
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		try:
			c.execute("\
insert into catagory (name,board_id) values (?,?);",(catagory_name,self.id))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
			
	def move_article_to_catagory(self,article_id,catagory_id):
		try:
			article=self.articles[article_id]
		except (KeyError) as e:
			return False
		
		
		if catagory_id==None:
			article.catagory=None
		else:
			try:
				article.catagory=self.catagorys[catagory_id]
			except (KeyError) as e:
				return False
		
		return article.updatetodatabase()
			
		
		

		
		
	
			
	def delete_catagory(self,catagory_id):
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		try:
			c.execute("\
delete from catagory where id=?;",(catagory_id,))
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
	def getboard(id):
		"""从数据库中获取一整个板块
		"""
		
		conn=sqlite3.connect(DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		try:
			c.execute("\
select \
	board.id as board_id, \
	board.name as board_name, \
	catagory.id as catagory_id, \
	catagory.name as catagory_name \
from \
	board left join catagory \
		on catagory.board_id=board.id \
where board.id=? \
order by catagory.id desc;",\
(id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.close()
			return None
		else:
			catagory_rows=c.fetchall()
			
			if len(catagory_rows)==0:
				return None
			
			board=Board(id,catagory_rows[0]["board_name"],collections.OrderedDict(),collections.OrderedDict())
			
			for catagory_row in catagory_rows:
				catagory_id=catagory_row["catagory_id"]
				catagory_name=catagory_row["catagory_name"]
				if catagory_id!=None:
					one_catagory=Catagory(catagory_id,catagory_name,board)
					board.catagorys[one_catagory.id]=one_catagory
					
			if len(board.catagorys)==0:
				board.catagorys=None
		
		try:
			c.execute("\
select \
	article.id as article_id, \
	article.time as article_time, \
	article.title as article_title, \
	article.abstract as article_abstract, \
	article.content as article_content, \
	article.source as article_source, \
	article.stick_index as article_stick_index, \
	article.title_bold as article_title_bold, \
	article.stick_index as article_stick_index, \
	article.catagory_id as article_catagory_id, \
	quicklinks.id as quicklinks_id \
from \
	article left join quicklinks \
		on article.id=quicklinks.article_id \
where article.board_id=? \
order by article.stick_index desc, article.id desc;", \
(id,))
		except (sqlite3.DatabaseError) as e:
			print e
			return board
		else:
			article_rows=c.fetchall()
		finally:
			conn.close
			
		for article_row in article_rows:
			article_id=article_row["article_id"]
			article_time=article_row["article_time"]
			article_title=article_row["article_title"]
			article_abstract=article_row["article_abstract"]
			article_content=article_row["article_content"]
			article_source=article_row["article_source"]
			article_title_bold=article_row["article_title_bold"]
			article_catagory_id=article_row["article_catagory_id"]
			article_recommended=article_row["quicklinks_id"]
			article_stick_index=article_row["article_stick_index"]
			
			if article_id==None:
				break
			
			if article_catagory_id != None:
				try:
					article_catagory=board.catagorys[article_catagory_id]
				except (KeyError):
					article_catagory=None
			else:
				article_catagory=None
				
			if article_recommended==None:
				article_recommended=False
			else:
				article_recommended=True
				
			if article_title_bold==1:
				article_title_bold=True
			else:
				article_title_bold=False
				
			
			
			one_article=article.Article(id=article_id,\
								title=article_title,\
								forum=board,\
								time=article_time,\
								abstract=article_abstract,\
								content=article_content,\
								source=article_source,\
								title_bold=article_title_bold,\
								catagory=article_catagory,\
								recommended=article_recommended,\
								sticked=article_stick_index)
			
			board.articles[one_article.id]=one_article
			
		if len(board.articles)==0:
				board.articles=None
				
		return board
			
		
			
			
			
		
