# -*- coding: utf-8 -*-
import sqlite3
import board
import datetime
from lxml.html.clean import Cleaner

class Article(object):
	def __init__(self,id,title,forum,time=None,abstract=None,content=None,source=None,title_bold=False,catagory=None,recommended=False,sticked=False):
	
		self.id=id
		self.title=title
		if time==None:
			self.time=unicode(datetime.date.today())
		else:
			self.time=time
		self.forum=forum
		self.abstract=abstract
		self.content=content
		self.source=source
		self.title_bold=title_bold
		self.catagory=catagory
		self.recommended=recommended
		self.sticked=sticked
	
	def __unicode__(self):
		result=u"id:"+unicode(self.id)+u";\ntitle:"+unicode(self.title)+u";\nforum_name:"+unicode(self.forum.name)+u";\nforum_id:"+unicode(self.forum.id)+u";\ntime:"+self.time+u";\nabstract:"+unicode(self.abstract)+u";\nsource:"+unicode(self.source)+u";\ncontent:"+unicode(self.content)
		return result
		
	def inserttodatabase(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		
		try:
			if self.catagory!=None:
				c.execute("\
insert into article (title,time,abstract,content,source,board_id,catagory_id) values (?,?,?,?,?,?,?)",\
(self.title,self.time,self.abstract,self.content,self.source,self.forum.id,self.catagory.id))
			else:
				c.execute("\
insert into article (title,time,abstract,content,source,board_id,catagory_id) values (?,?,?,?,?,?,?)",\
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
			
		
	def get_abstract(self):
		cleaner = Cleaner(page_structure=True, links=True,style=True,safe_attrs_only=True,scripts=True, embedded=True, meta=True,remove_tags = ["a","abbr","acronym","address","applet","area","article","aside","audio","b","base","basefont","bdi","bdo","big","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","command","datalist","dd","del","details","dfn","dialog","dir","div","dl","dt","em","embed","fieldset","figcaption","figure","font","footer","form","frame","frameset","h1",-"h6","head","header","hr","html","i","iframe","img","input","ins","kbd","keygen","label","legend","li","link","main","map","mark","menu","menuitem","meta","meter","nav","noframes","noscript","object","ol","optgroup","option","output","p","param","pre","progress","q","rp","rt","ruby","s","samp","script","section","select","small","source","span","strike","strong","style","sub","summary","sup","table","tbody","td","textarea","tfoot","th","thead","time","title","tr","track","tt","u","ul","var","video","wbr"],frames=True,forms=True,annoying_tags=True)
		return cleaner.clean_html(self.content).lstrip("<div>").lstrip()[0:150]
		
	
	def updatetodatabase(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		
		try:
			if self.catagory!=None:
				c.execute("\
update article set title=?,abstract=?,content=?,source=?,catagory_id=? where id=?;",\
(self.title,self.abstract,self.content,self.source,self.catagory.id,self.id))
			else:
				c.execute("\
update article set title=?,abstract=?,content=?,source=?,catagory_id=? where id=?;",\
(self.title,self.abstract,self.content,self.source,None,self.id))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
			
	def deletetodatabase(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		
		try:
			c.execute("\
delete from article where id=?;",\
(self.id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
			
	def recommend(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
insert into quicklinks (board_id,article_id) values (?,?);\
",(self.forum.id,self.id))
		except	(sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
		
	def unrecommend(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
delete from quicklinks where article_id=?;\
",(self.id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()

	def bold(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
update article set title_bold=1 where id=?;\
",(self.id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
			
	def unbold(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
update article set title_bold=0 where id=?;\
",(self.id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			self.title_bold=True
			return True
		finally:
			conn.close()
			
	def stick(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
select \
	max(stick_index) as max_stick_index \
from \
	article \
where \
	board_id=?;",(self.forum.id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.close()
			return False
		else:
			max_stick_index_row=c.fetchone()
			max_stick_index=max_stick_index_row["max_stick_index"]
			if max_stick_index==None:
				next_max_stick_index=1
			else:
				next_max_stick_index=max_stick_index+1
		
		try:
			c.execute("\
update article set stick_index=? where id=?;",(next_max_stick_index,self.id))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
		
	
	def unstick(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
update article set stick_index=null where id=?;",(self.id,))
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
		conn=sqlite3.connect(board.DatabasePath)
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
	article.title_bold as article_title_bold, \
	board.id as board_id, \
	board.name as board_name, \
	catagory.id as catagory_id,\
	catagory.name as catagory_name,  \
	quicklinks.id as quicklinks_id \
from \
	article inner join board on \
		board.id=article.board_id \
	left join catagory on \
		catagory.id=article.catagory_id and catagory.board_id=board.id \
	left join quicklinks on \
		article.id=quicklinks.article_id \
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
		
		all_forum=board.Forum.get_all_forum()
		tempforum=all_forum[row["board_id"]]
		
		if row["catagory_id"]!=None:
			tempcatagory=board.Catagory(row["catagory_id"],row["catagory_name"],tempforum)
		else:
			tempcatagory=None  #没有catagory
			
		article_title_bold=(row["article_title_bold"]==1 and True) or False
		article_recommended=row["quicklinks_id"]
		if article_recommended==None:
			article_recommended=True
		else:
			article_recommended=False
		
		result=Article(id=row["article_id"],\
						time=row["article_time"],\
						title=row["article_title"],\
						forum=tempforum,\
						abstract=row["article_abstract"],\
						content=row["article_content"],\
						source=row["article_source"],\
						title_bold=row["article_title_bold"],\
						catagory=tempcatagory,\
						recommended=article_recommended)
		
		return result
