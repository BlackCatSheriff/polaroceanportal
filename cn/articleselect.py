# -*- coding: utf-8 -*-
from board import Board
import collections
PageArticleCount=10


def add_board_pagesize(func):
	def wrapper(*args,**kw):
		result=func(*args,**kw)
		if result.articles==None:
			result.pagecount=None
			return result
			
		if len(result.articles) % PageArticleCount >0:
			result.pagecount=len(result.articles)/PageArticleCount + 1
		else:
			result.pagecount=len(result.articles)/PageArticleCount
		return result
		
	return wrapper

@add_board_pagesize
def select_by_catagory(board,catagory_id):
	if board.articles==None:
		return board
		
	elif catagory_id==None:
		return board
		
	else:
		new_board=Board(board.id,board.name)
		new_board.catagorys=board.catagorys
		new_board.articles=collections.OrderedDict()
		for article_id,article in board.articles.iteritems():
			if article.catagory==None:
				continue
			
			if article.catagory.id==catagory_id:
				new_board.articles[article.id]=article
		
		if len(new_board.articles)==0:
			new_board.articles=None
		return new_board
				
	

def select_by_page(board,page_id):
	if page_id==None:
		page_id=1
		
	for i in range(0,PageArticleCount*(page_id-1)):
		try:
			board.articles.popitem(False)
		except (KeyError):
			board.articles=None
			break
	
	return board

def test():
	return select_by_catagory(data.forums[2],2)
