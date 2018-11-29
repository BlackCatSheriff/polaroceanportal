# -*- coding: utf-8 -*-
import sqlite3
import board
import datetime
import re
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
		#cleaner = Cleaner(page_structure=True, links=True,style=True,safe_attrs_only=True,scripts=True, embedded=True, meta=True,remove_tags = ["b","i","div","small","blockquote","a","p","h1","h2","h3","h4","br","u","img"],frames=True,forms=True,annoying_tags=True)
		#return cleaner.clean_html(self.content).lstrip("<div>").lstrip()[0:150]
		def filter_tags(htmlstr):
		    #先过滤CDATA
		    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
		    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
		    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
		    re_br=re.compile('<br\s*?/?>')#处理换行
		    re_h=re.compile('</?\w+[^>]*>')#HTML标签
		    re_comment=re.compile('<!--[^>]*-->')#HTML注释
		    s=re_cdata.sub('',htmlstr)#去掉CDATA
		    s=re_script.sub('',s) #去掉SCRIPT
		    s=re_style.sub('',s)#去掉style
		    s=re_br.sub('\n',s)#将br转换为换行
		    s=re_h.sub('',s) #去掉HTML 标签
		    s=re_comment.sub('',s)#去掉HTML注释
		    #去掉多余的空行
		    blank_line=re.compile('\n+')
		    s=blank_line.sub('\n',s)
		    s=replaceCharEntity(s)#替换实体
		    return s

		##替换常用HTML字符实体.
		#使用正常的字符替换HTML中特殊的字符实体.
		#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
		#@param htmlstr HTML字符串.
		def replaceCharEntity(htmlstr):
		    CHAR_ENTITIES={'nbsp':' ','160':' ',
				'lt':'<','60':'<',
				'gt':'>','62':'>',
				'amp':'&','38':'&',
				'quot':'"','34':'"',}
		   
		    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
		    sz=re_charEntity.search(htmlstr)
		    while sz:
			entity=sz.group()#entity全称，如&gt;
			key=sz.group('name')#去除&;后entity,如&gt;为gt
			try:
			    htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
			    sz=re_charEntity.search(htmlstr)
			except KeyError:
			    #以空串代替
			    htmlstr=re_charEntity.sub('',htmlstr,1)
			    sz=re_charEntity.search(htmlstr)
		    return htmlstr

		def repalce(s,re_exp,repl_string):
		    return re_exp.sub(repl_string,s)
		dealStr = filter_tags(self.content) 
		if len(dealStr) > 150:
			return dealStr[0:150]
		return dealStr

		
	
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
