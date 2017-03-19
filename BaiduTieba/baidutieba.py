# -*- coding:utf-8 -*-
__author__ = 'CQC'
import urllib
import urllib2
import re
#处理页面标签
class Tool:
    removeImg=re.compile('<img.*?>| {7}|')#去掉img标签和7位长空格
    removeAddr=re.compile('<a.*?>|</a>')#去掉超链接标签
	 #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

    
#自定义：百度贴吧类
class BDTB:
	#初始化，传入基地址，是否只看楼主的参数
	def __init__(self,baseurl,see_lz,floorTag):
		#对self的各项属性初始化
		self.baseURL=baseurl
		self.seeLZ='?see_lz='+str(seeLZ)#是否只看楼主
		self.tool=Tool()#实例tool对象
		self.file=None#全局file对象，写入内容的文件
		self.floor=1#楼层标号，初始为1
		self.defaultTitle= "百度贴吧"
		#默认标题,如果没有成功获取到标题的话就用这个
		self.floorTag=floorTag#是否写入楼层信息
	
	#传入页码，构建url，获取当前页面代码到page
	def getPage(self,pageNum):
		try:
			url=self.baseURL+self.seeLZ+'&pn=' + str(pageNum)
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
			#
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print "连接错误",e.reason
				return None	
	#获取帖子标题
	def getTitle(self,page):
		#标题的正则表达式
		#pattern=re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
		#pattern = re.compile('<h3 class=core_title_txt.*?>(.*?)</h3>',re.S)
		pattern = re.compile('<title.*?>(.*?)</title>',re.S)
		result=re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None
	
	#获取帖子一共多少页
	def getPageNum(self,page):
		#获取帖子页数的正则表达式
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None

	
	#为文件设置标题
	def setFileTitle(self,title):
		if title is not None:
			self.file=open(title+".txt","w+")
		else:
			self.file=open(self.defaultTitle+".txt","w+")
	
	#向文件写入每一层楼的信息
	def writeData(self,contents):
		for item in contents:
			if self.floorTag=='1':
				floorline="\n"+str(self.floor)+"---------------\n"#分隔线
				self.file.write(floorline)
			self.file.write(item)
			self.floor+=1
	
	#从当前的page得到的代码中进行清理，存储到contents
	def getContent(self,page):
		pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items=re.findall(pattern,page)
		contents=[]
		for item in items:
			content="\n"+self.tool.replace(item)+"\n"
			contents.append(content.encode('utf-8'))
		return contents
	
	#
	def start(self):
		#初始化得到第一页的代码，并且从中获取标题和页数
		indexpage=self.getPage(1)
		pageNum=self.getPageNum(indexpage)
		title=self.getTitle(indexpage)
		
		#设置文件标题
		self.setFileTitle(title)
		if pageNum==None:
			print "URL已经失效"
			return 
		try:
			print "该帖子共有"+str(pageNum)+"页"
			#循环从每页中获取内容，写入文件
			for i in range(1,int(pageNum)+1):
				print "正在写入第"+str(i)+"页"
				page=self.getPage(i)
				contents=self.getContent(page)
				self.writeData(contents)
		except IOError,e:
			print "写入异常"+e.message
		finally:
			print "任务完成"
		
	

#--------------主函数
print "请输入帖子号码"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)#构造函数传入参数实例BDTB对象
bdtb.start()#调用类中的start（），开始
	


