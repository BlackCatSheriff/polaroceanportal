#-*- coding: utf-8 -*-

import sqlite3
import hashlib
import board
import collections

def login_user(session,user_name,user_passwd):
	user=User.get_user(user_name,user_passwd)
	if user:
		session["user_id"]=user.id
		session["user_name"]=user.name
		return user
	else:
		return False
	
def logout_user(session):
	session.pop('user_name', None)
	session.pop('user_id', None)
	
	
def check_login_state(session):
	if "user_name" in session and "user_id" in session:
		return User(session["user_id"],session["user_name"])
	else:
		return None
	

class User(object):
	def __init__(self,id,name):
		self.id=id
		self.name=name
		
	def change_passwd(self,new_user_passwd):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		md5=hashlib.md5()
		md5.update(new_user_passwd)
		encrypted_passwd=md5.hexdigest()
		
		try:
			c.execute("\
update users set passwd=? where name=?;",\
(encrypted_passwd,self.name))
			
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
		
	def get_all_user(self):
		if self.name!="Administrator":
			return False
			
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
select \
	id as user_id,\
	name as user_name \
from \
	users;")
		except (sqlite3.DatabaseError) as e:
			print e
			return False
		else:
			user_rows=c.fetchall()
			result=collections.OrderedDict()
			for user_row in user_rows:
				user=User(user_row["user_id"],user_row["user_name"])
				result[user.id]=user
			if len(result)==0:
				result=None
				
			return result
			
			
		finally:
			conn.close()
		
	
	def delete_user(self,user_name):
		if self.name!="Administrator":
			return False
			
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
delete from users where name=?;",\
(user_name,))
		except (sqlite3.Database) as e:
			print e
			conn.rollback()
			return False
		else:
			conn.commit()
			return True
		finally:
			conn.close()
		
	def create_user(self,new_user_name,new_user_passwd):
		if self.name!="Administrator":
			return False
			
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		md5=hashlib.md5()
		md5.update(new_user_passwd)
		encrypted_passwd=md5.hexdigest()
		
		try:
			c.execute("\
insert into users (name,passwd) values (?,?);",\
(new_user_name,encrypted_passwd))
			c.execute("select last_insert_rowid() as user_id from users;")
			
		except (sqlite3.DatabaseError) as e:
			print e
			conn.rollback()
			return False
		else:
			new_user_id_row=c.fetchone()
			if new_user_id_row==None:
				result=False
				conn.rollback()
			else:
				new_user_id=new_user_id_row["user_id"]
				result=User(new_user_id,new_user_name)
				conn.commit()
			return result
		finally:
			conn.close()
			
		
	def reset_passwd(self,user_name,new_user_passwd):
		if self.name!="Administrator":
			return False
			
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		md5=hashlib.md5()
		md5.update(new_user_passwd)
		encrypted_passwd=md5.hexdigest()
		
		try:
			c.execute("\
update users set passwd=? where name=?;",\
(encrypted_passwd,user_name))
			
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
	def get_user(user_name,user_passwd):
		conn=sqlite3.connect(board.DatabasePath)
		conn.row_factory=sqlite3.Row
		conn.execute("pragma foreign_key=on")
		c=conn.cursor()
		
		try:
			c.execute("\
select \
	id as user_id, \
	name as user_name, \
	passwd as user_passwd \
from \
	users \
where name=?;",\
(user_name,))
		except (sqlite3.DatabaseError) as e:
			print e
			return None
		else:
			user_row=c.fetchone()
			if user_row==None:
				return None
			else:
				real_passwd=user_row["user_passwd"]
				user_id=user_row["user_id"]
				
				md5=hashlib.md5()
				md5.update(user_passwd)
				
				if real_passwd==md5.hexdigest():
					result=User(user_id,user_name)
					
				else:
					result=False
				return result
				
		finally:
			conn.close()
			
		
	
