# -*- coding:utf-8 -*-
__author__ = 'CQC'
import urllib
import urllib2
import re
#����ҳ���ǩ
class Tool:
    removeImg=re.compile('<img.*?>| {7}|')#ȥ��img��ǩ��7λ���ո�
    removeAddr=re.compile('<a.*?>|</a>')#ȥ�������ӱ�ǩ
	 #�ѻ��еı�ǩ��Ϊ\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #������Ʊ�<td>�滻Ϊ\t
    replaceTD= re.compile('<td>')
    #�Ѷ��俪ͷ��Ϊ\n�ӿ�����
    replacePara = re.compile('<p.*?>')
    #�����з���˫���з��滻Ϊ\n
    replaceBR = re.compile('<br><br>|<br>')
    #�������ǩ�޳�
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()��ǰ���������ɾ��
        return x.strip()

    
#�Զ��壺�ٶ�������
class BDTB:
	#��ʼ�����������ַ���Ƿ�ֻ��¥���Ĳ���
	def __init__(self,baseurl,see_lz,floorTag):
		#��self�ĸ������Գ�ʼ��
		self.baseURL=baseurl
		self.seeLZ='?see_lz='+str(seeLZ)#�Ƿ�ֻ��¥��
		self.tool=Tool()#ʵ��tool����
		self.file=None#ȫ��file����д�����ݵ��ļ�
		self.floor=1#¥���ţ���ʼΪ1
		self.defaultTitle= "�ٶ�����"
		#Ĭ�ϱ���,���û�гɹ���ȡ������Ļ��������
		self.floorTag=floorTag#�Ƿ�д��¥����Ϣ
	
	#����ҳ�룬����url����ȡ��ǰҳ����뵽page
	def getPage(self,pageNum):
		try:
			url=self.baseURL+self.seeLZ+'&pn=' + str(pageNum)
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
			#
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print "���Ӵ���",e.reason
				return None	
	#��ȡ���ӱ���
	def getTitle(self,page):
		#�����������ʽ
		#pattern=re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
		#pattern = re.compile('<h3 class=core_title_txt.*?>(.*?)</h3>',re.S)
		pattern = re.compile('<title.*?>(.*?)</title>',re.S)
		result=re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None
	
	#��ȡ����һ������ҳ
	def getPageNum(self,page):
		#��ȡ����ҳ����������ʽ
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None

	
	#Ϊ�ļ����ñ���
	def setFileTitle(self,title):
		if title is not None:
			self.file=open(title+".txt","w+")
		else:
			self.file=open(self.defaultTitle+".txt","w+")
	
	#���ļ�д��ÿһ��¥����Ϣ
	def writeData(self,contents):
		for item in contents:
			if self.floorTag=='1':
				floorline="\n"+str(self.floor)+"---------------\n"#�ָ���
				self.file.write(floorline)
			self.file.write(item)
			self.floor+=1
	
	#�ӵ�ǰ��page�õ��Ĵ����н��������洢��contents
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
		#��ʼ���õ���һҳ�Ĵ��룬���Ҵ��л�ȡ�����ҳ��
		indexpage=self.getPage(1)
		pageNum=self.getPageNum(indexpage)
		title=self.getTitle(indexpage)
		
		#�����ļ�����
		self.setFileTitle(title)
		if pageNum==None:
			print "URL�Ѿ�ʧЧ"
			return 
		try:
			print "�����ӹ���"+str(pageNum)+"ҳ"
			#ѭ����ÿҳ�л�ȡ���ݣ�д���ļ�
			for i in range(1,int(pageNum)+1):
				print "����д���"+str(i)+"ҳ"
				page=self.getPage(i)
				contents=self.getContent(page)
				self.writeData(contents)
		except IOError,e:
			print "д���쳣"+e.message
		finally:
			print "�������"
		
	

#--------------������
print "���������Ӻ���"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("�Ƿ�ֻ��ȡ¥�����ԣ�������1��������0\n")
floorTag = raw_input("�Ƿ�д��¥����Ϣ��������1��������0\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)#���캯���������ʵ��BDTB����
bdtb.start()#�������е�start��������ʼ
	


