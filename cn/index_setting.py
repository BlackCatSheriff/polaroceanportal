# -*- coding:utf-8 -*-

import sqlite3
import board
import collections

class Jumbotron(object):
	def __init__(self,title,content,link,imagelink):
		self.title=title
		self.content=content
		self.link=link
		self.image_link=imagelink
		self.key=1
	
	def updatetodatabase(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		try:
			c.execute("\
update setting set value=? where key=? and name=?;",\
(self.title,self.key,"jumbotron_title"))
			c.execute("\
update setting set value=? where key=? and name=?;",\
(self.content,self.key,"jumbotron_content"))
			c.execute("\
update setting set value=? where key=? and name=?;",\
(self.link,self.key,"jumbotron_link"))
			c.execute("\
update setting set value=? where key=? and name=?;",\
(self.image_link,self.key,"jumbotron_image_link"))
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
	def getfromdatabase():
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		try:
			c.execute("\
select \
	setting1.id,\
	setting1.key,\
	setting1.name,\
	setting1.value as jumbotron_title,\
	setting2.name,\
	setting2.value as jumbotron_content,\
	setting3.name,\
	setting3.value as jumbotron_link,\
	setting4.name,\
	setting4.value as jumbotron_image_link \
from \
	setting as setting1 inner join setting as setting2\
	inner join setting as setting3 inner join\
	setting as setting4 \
where \
	setting1.key=? and setting1.name=? and setting2.name=? and setting3.name=? and setting4.name=?",\
(1,"jumbotron_title","jumbotron_content","jumbotron_link","jumbotron_image_link"))
		except (sqlite3.DatabaseError) as e:
			print e
			return None
		else:
			row=c.fetchone()
			jumbotron_title=row["jumbotron_title"]
			jumbotron_content=row["jumbotron_content"]
			jumbotron_link=row["jumbotron_link"]
			jumbotron_image_link=row["jumbotron_image_link"]
			result=Jumbotron(jumbotron_title,jumbotron_content,jumbotron_link,jumbotron_image_link)
			return result
		finally:
			conn.close()

class Slick(object):
	def __init__(self,key,name):
		self.name=name
		self.key=key
		self.items=None
		
	def get_item(self,item_id):
		self.populate_items()
		try:
			result=self.items[item_id]
		except (KeyError,TypeError):
			result=None
			return result
		else:
			return result
		
	def create_item(self,item_name,item_link,item_image_link):
		if self.items==None:
			self.populate_items()
		
		if self.items==None:
			self.items=collections.OrderedDict()
		
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		
		
		try:
			c.execute("\
insert into setting (key,name,value) values (?,?,?);",\
(self.key,"name",item_name))
			c.execute("select last_insert_rowid() as item_id from setting;")
			name_row_id_row=c.fetchone()
			name_row_id=name_row_id_row["item_id"]
			
			c.execute("\
update setting set parent_id=? where id=?;",\
(name_row_id,name_row_id))
			c.execute("\
insert into setting (key,name,value,parent_id) values (?,?,?,?);",\
(self.key,"link",item_link,name_row_id))
			c.execute("\
insert into setting (key,name,value,parent_id) values (?,?,?,?);",\
(self.key,"image_link",item_image_link,name_row_id))
			
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return None
			
		else:
			conn.commit()
			result=Item(name_row_id,item_name,item_link,item_image_link,self)
			
			self.items[result.id]=result
			
			return result
			
		finally:
			conn.close()
			
	def populate_items(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		
		try:
			c.execute("\
select \
	setting1.id as item_id,\
	setting1.key,\
	setting1.parent_id,\
	setting1.name,\
	setting1.value as item_name,\
	setting2.name, \
	setting2.value as item_link, \
	setting3.name,\
	setting3.value as item_image_link \
from \
	setting as setting1 inner join setting as setting2 \
		on setting1.id=setting2.parent_id \
	inner join setting as setting3 \
		on setting2.parent_id=setting3.parent_id \
where setting1.name=? and setting2.name=? and setting3.name=? and setting1.key=? \
order by setting1.id;",\
("name","link","image_link",self.key))

		except (sqlite3.DatabaseError) as e:
			print e
			self.items=None
			return False
		else:
			rows=c.fetchall()
			if rows==None or len(rows)==0:
				self.items=None
				return True
				
			self.items=collections.OrderedDict()
			
			
			for row in rows:
				item_id=row["item_id"]
				item_name=row["item_name"]
				item_link=row["item_link"]
				item_image_link=row["item_image_link"]
				item=Item(item_id,item_name,item_link,item_image_link,self)
				
				self.items[item.id]=item
			return True

class Item(object):
	def __init__(self,id,name,link,image_link,slick):
		self.id=id
		self.name=name
		self.link=link
		self.image_link=image_link
		self.slick=slick
		
	def delete(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		try:
			c.execute("\
delete from setting where key=? and parent_id=?;",\
(self.slick.key,self.id))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			self.slick.items.pop(self.id)
			self=None
			return True
		finally:
			conn.close()
	
	def update(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		try:
			c.execute("\
update setting set value=? where key=? and parent_id=? and name=?;",\
(self.name,self.slick.key,self.id,"name"))
			c.execute("\
update setting set value=? where key=? and parent_id=? and name=?;",\
(self.link,self.slick.key,self.id,"link"))
			c.execute("\
update setting set value=? where key=? and parent_id=? and name=?;",\
(self.image_link,self.slick.key,self.id,"image_link"))		
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
			
class Aboutus():
	def __init__(self,id,address):
		self.id=id
		self.address=address
		self.key=4
	
	@staticmethod
	def get_from_database():
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		try:
			c.execute("\
select \
	id as aboutus_id, \
	value as aboutus_address \
from \
	setting \
where \
	key=4;")
		except (sqlite3.DatabaseError) as e:
			print e
			return False
		else:
			aboutus_row=c.fetchone()
			if aboutus_row==None:
				return False
			else:
				aboutus_id=aboutus_row["aboutus_id"]
				aboutus_address=aboutus_row["aboutus_address"]
				result=Aboutus(aboutus_id,aboutus_address)
				return result
		finally:
			conn.close()
	
	def update_to_database(self):
		conn=sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory=sqlite3.Row
		c=conn.cursor()
		try:
			c.execute("\
update setting set value=? where id=?",(self.address,self.id))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()


class Footer(object):
	def __init__(self):
		self.key = 5
		self.items = None

	def get_item(self, item_id):
		self.populate1_items()
		try:
			result = self.items[item_id]
		except (KeyError, TypeError):
			result = None
			return result
		else:
			return result

	def create_item(self, item_name, item_link):
		if self.items == None:
			self.populate1_items()

		if self.items == None:
			self.items = collections.OrderedDict()

		conn = sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		try:
			c.execute("\
insert into setting (key,name,value) values (?,?,?);", \
					  (5, item_name,item_link))
			c.execute("select last_insert_rowid() as item_id from setting;")
			name_row_id_row = c.fetchone()
			name_row_id = name_row_id_row["item_id"]

		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return None

		else:
			conn.commit()
			result = FooterItem(name_row_id, item_name, item_link)

			self.items[result.id] = result

			return result

		finally:
			conn.close()

	def populate1_items(self):
		conn = sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		try:
			c.execute("\
			select \
				id as item_id, \
				name as item_name,\
				value as item_link \
			from \
				setting \
			where \
				key=5;")

		except (sqlite3.DatabaseError) as e:
			print e
			self.items = None
			return False
		else:
			rows = c.fetchall()
			if rows == None or len(rows) == 0:
				self.items = None
				return True

			self.items = collections.OrderedDict()

			for row in rows:
				item_id = row["item_id"]
				item_name = row["item_name"]
				item_link = row["item_link"]
				item = FooterItem(item_id, item_name, item_link)

				self.items[item.id] = item
			return True


class FooterItem(object):
	def __init__(self, id, name, link):
		self.id = id
		self.name = name
		self.link = link


	def delete(self):
		conn = sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		try:
			c.execute("\
delete from setting where id=?;\
			", (self.id,))
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			# self.footer.items.pop(self.id)
			self = None
			return True
		finally:
			conn.close()

	def update(self):
		conn = sqlite3.connect(board.DatabasePath)
		conn.execute("pragma foreign_key=on")
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		try:
			c.execute("\
update setting set name=?,value=? where id=?;", \
					  (self.name, self.link, self.id))

		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()

footerList=Footer()
professors=Slick(key=3,name=u"professors")
professors.chinese_name=u"顾问学者"
scholars=Slick(key=2,name=u"scholars")
scholars.chinese_name=u"研究团队"
