#-*- coding: utf-8 -*-

class Message(object):
	def __init__(self,id,description,type):
		self.id=id
		self.description=description
		self.type=type
	
	def detail(self,detail):
		self.description=self.description+detail
		
def get_message(args):
	try:
		message_id=int(args["message"])
	except (KeyError,ValueError):
		message=None
	else:
		message=get_message_by_id(message_id)
		
	return message
		
success=Message(1,u"操作成功",1)
failed=Message(2,u"操作失败",-1)
warning=Message(3,u"注意",2)
error=Message(4,u"错误",-2)
_allmessages={}
_allmessages[success.id]=success
_allmessages[failed.id]=failed
_allmessages[warning.id]=warning
_allmessages[error.id]=error

def get_message_by_id(id):
	return _allmessages[id]
