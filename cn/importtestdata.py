# -*- coding: utf-8 -*-
import sqlite3

def importdata():
	conn=sqlite3.connect("database")
	conn.execute("pragma foreign_key=on")
	c=conn.cursor()
	for i in range(1,5):
		c.execute("insert into article (time,title,abstract,content,source,forum_id) values (?,?,?,?,?,?)",("time:"+str(i),"title:"+str(i),"abstract:"+str(i),"content:"+str(i),"source:"+str(i),2))
	conn.commit()
	conn.close()
		
		
def getdata():
	conn=sqlite3.connect("database")
	conn.row_factory=
	conn.execute("pragma foreign_key=on")
	c=conn.cursor()
	c.execute("select * from article inner join forum on forum.id=article.forum_id where article.id=?",(1,))
	return c
