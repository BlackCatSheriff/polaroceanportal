#-*- coding:utf-8 -*-
from oss.oss_api import *
from oss import oss_xml_handler
import collections

endpoint="oss-cn-qingdao.aliyuncs.com"
accessKeyId,accessKeySecret="USv7TZpxSJC2FISB","i9ZM5kQlIhzmmpf58sY5dW8NOBSocr"
oss=OssAPI(endpoint,accessKeyId,accessKeySecret)

Buckets_Name_Map={u"image":("pop-upload-image",u"图片"),u"file":(u"pop-upload-files",u"其他文件")}



def test():
	Bucket.get_bucket(Upload_Image_Bucket_Name)
	
class Bucket(object):
	def __init__(self,name):
		self.name=name
		self.directorys=collections.OrderedDict()
		self.raw_name=Buckets_Name_Map[self.name][0]
		self.chinese_name=Buckets_Name_Map[self.name][1]
	
	def create_dir(self,dir_name):
		
		res=oss.put_object_from_string(self.raw_name,dir_name+"/","")
		if res.status/100==2:
			return True
		else:
			return False
	
	def get_dir(self,dir_name):
	
		try:
			result=self.directorys[dir_name]
			result.fill()
		except (KeyError):
			return None
		
		return result
	
	
	@staticmethod
	def get_bucket(name):
		
		try:
			result=Bucket(name)
		except (KeyError):
			return None

		res=oss.list_bucket(result.raw_name,delimiter="/")
		objects_xml=oss_xml_handler.GetBucketXml(res.read())
		
		
		for prefix in objects_xml.prefix_list:
			one_dir=Directory(prefix,result)
			result.directorys[one_dir.name]=one_dir
		
		return result
		
class Directory(object):
	def __init__(self,name,bucket):
		self.raw_name=name
		self.name=name.rstrip("/")
		self.bucket=bucket
		self.files=collections.OrderedDict()
	
	def create_file(self,f):
		res=oss.put_object_from_fp(self.bucket.raw_name,self.raw_name+f.filename,f)
		if res.status/100==2:
			return True
		else:
			return False
		
	def delete(self):
		if len(self.files)>0:
			return False
			
		else:
			res=oss.delete_object(self.bucket.raw_name,self.raw_name)
			if res.status/100==2:
				return True
			else:
				return False
	
	def get_file(self,file_name):
		try:
			result=self.files[file_name]
		except (KeyError):
			return None
		
		return result
		
	def fill(self):
		res=oss.list_bucket(self.bucket.raw_name,prefix=self.raw_name)
		objects_xml=oss_xml_handler.GetBucketXml(res.read())
		for object_info in objects_xml.content_list:
			if object_info.key!=self.raw_name:
				one_file=File(object_info.key,self,object_info.last_modified)
				self.files[one_file.name]=one_file
		
class File(object):
	def __init__(self,name,directory,last_modified_time=None):
		self.directory=directory
		self.raw_name=name
		self.name=name.lstrip(directory.name).lstrip("/")
		self.last_modified_time=last_modified_time
		
	def delete(self):
		res=oss.delete_object(self.directory.bucket.raw_name,self.raw_name)
		if res.status/100==2:
			return True
		else:
			return False
