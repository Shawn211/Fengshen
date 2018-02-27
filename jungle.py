#coding=utf-8

import requests
import re
from lxml import etree
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fs='http://www.mfengshen.com/'
play1='http://www.mfengshen.com/wapgame.php?sid='
play2='http://www.mfengshen.com/wapgame.php?sid='
play3='http://www.mfengshen.com/wapgame.php?sid='
headers={'Cookie':''}

money=0
experience=0
times=0

FLAG=0

def login(player):
	FLAG=0

	lg0=requests.get(player,headers=headers).content
	#print lg0.decode('utf-8')
	lg0=etn(lg0)
	#print lg0.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
	url0=searchurl(lg0,'封妖师OL一区-奇迹世界')
	#print url0

	lg1=requests.get(url0,headers=headers).content
	#print lg1.decode('utf-8')
	if re.search('欢迎回家',lg1):
		print re.search(r'(欢迎回家,.*!)<br />',lg1).group(1).decode('utf-8')
		lg1=etn(lg1)
		#print lg1.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
		url1=searchurl(lg1,'我回来了')

		lg2=requests.get(url1,headers=headers).content
		#print lg2.decode('utf-8')
		lg2=etn(lg2)
		#print lg2.xpath('string(//body)').decode('utf-8')      #显示页面内容，后期删除
		gameurl=searchurl(lg2,'进入游戏')

		if gameurl:
			print u'您已登录成功！'
		return gameurl,FLAG

	elif re.search('刷新',lg1):
		print u'您仍在线！'
		lg1=etn(lg1)
		gameurl=searchurl(lg1,'刷新')

		return gameurl,FLAG

	elif re.search('进入游戏',lg1):
		print u'您仍在线！'
		lg1=etn(lg1)
		gameurl=searchurl(lg1,'进入游戏')

		return gameurl,FLAG

	elif re.search('主人,现在的情况是:',lg1):
		print u'您正处于战斗状态！'
		lg1=etn(lg1)
		print lg1.xpath('string(//body)').decode('utf-8')
		url1=fs+'fengshen/'+lg1.xpath('//body//a/@href')[0]
		gameurl,FLAG=zhandou(url1)

		return gameurl,FLAG

	else:
		print 'Something wrong!!!'

def job(gurl,FLAG):
	time_start=time.time()

	gurl,FLAG=cure(gurl)

	while 1:
		html=requests.get(gurl,headers=headers).content
		if FLAG == 0:
			if re.search('灌江口封妖观 ',html):			#设置初始封妖馆地点
				html=etn(html)
				gurl=searchurl(html,'刷新')

				gurl=walk(gurl,'a')
				gurl=walk(gurl,'s')
				gurl=walk(gurl,'a')
				gurl=walk(gurl,'s')

				print '---------------------\n'+u'程序运行时长：'+str(int(time.time()-time_start))
				gurl,FLAG=jungle(gurl)

			elif re.search('灌江口修行场 ',html):			#设置战斗刷怪地点
				html=etn(html)
				gurl=searchurl(html,'刷新')

				print '---------------------\n'+u'程序运行秒数：'+str(int(time.time()-time_start))
				gurl,FLAG=jungle(gurl)

			else:
				print u'您不在封妖馆！也不在刷怪点！请抓紧设置！'
				html=etn(html)
				gurl=searchurl(html,'刷新')

				print '---------------------\n'+u'程序运行时长：'+str(int(time.time()-time_start))
				gurl,FLAG=jungle(gurl)

		elif FLAG == 1:
			if re.search('灌江口封妖观 ',html):			#设置初始封妖馆地点
				html=etn(html)
				gurl=searchurl(html,'刷新')

				gurl,FLAG=cure(gurl)

			elif re.search('灌江口修行场 ',html):			#设置战斗刷怪地点
				html=etn(html)
				gurl=searchurl(html,'刷新')

				gurl=walk(gurl,'w')
				gurl=walk(gurl,'d')
				gurl=walk(gurl,'w')
				gurl=walk(gurl,'d')

				gurl,FLAG=cure(gurl)

			else:
				print u'您不在封妖馆！也不在刷怪点！请抓紧治疗！'
				html=etn(html)
				gurl=searchurl(html,'刷新')

	print u'任务完成！'

def cure(gurl):
	FLAG=1
	html=requests.get(gurl,headers=headers).content
	if re.search('治疗宠物',html):
		html=etn(html)
		gurl=searchurl(html,'治疗宠物')

		html=requests.get(gurl,headers=headers).content
		while re.search('等待',html):
			html=etn(html)
			gurl=searchurl(html,'等待')
			html=requests.get(gurl,headers=headers).content

		html=etn(html)
		gurl=searchurl(html,'返回游戏')
		FLAG=0
		return gurl,FLAG
	else:
		print u'您当前不在封妖馆！'
		html=etn(html)
		gurl=searchurl(html,'刷新')
		return gurl,FLAG

def walk(gurl,d):
	if d == 'w':
		html=requests.get(gurl,headers=headers).content
		if re.search(r'>北 .*↑</a>',html):
			html=etn(html)
			gurl=searchurl(html,'北 ')
			return gurl
		else:
			print u'此处没有北行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 'a':
		html=requests.get(gurl,headers=headers).content
		if re.search(r'>西 .*←</a>',html):
			html=etn(html)
			gurl=searchurl(html,'西 ')
			return gurl
		else:
			print u'此处没有西行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 'd':
		html=requests.get(gurl,headers=headers).content
		if re.search(r'>东 .*→</a>',html):
			html=etn(html)
			gurl=searchurl(html,'东 ')
			return gurl
		else:
			print u'此处没有东行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

	elif d == 's':
		html=requests.get(gurl,headers=headers).content
		if re.search(r'>南 .*↓</a>',html):
			html=etn(html)
			gurl=searchurl(html,'南 ')
			return gurl
		else:
			print u'此处没有南行走方向'
			html=etn(html)
			gurl=searchurl(html,'刷新')
			return gurl

def zhandou(zhandouurl):
	global money
	global experience
	global times
	FLAG=0
	zhandouhtml=requests.get(zhandouurl,headers=headers).content

	while not re.search('返回游戏',zhandouhtml):
		if re.search('没有足够的PP',zhandouhtml):
			FLAG=1

			zhandouhtml=etn(zhandouhtml)
			zhandouurl=searchurl(zhandouhtml,'逃跑')

			zhandouhtml=requests.get(zhandouurl,headers=headers).content

			while not re.search('返回游戏',zhandouhtml):
				zhandouhtml=etn(zhandouhtml)
				zhandouurl=searchurl(zhandouhtml,'逃跑')

				zhandouhtml=requests.get(zhandouurl,headers=headers).content

			zhandouhtml=etn(zhandouhtml)
			gameurl=searchurl(zhandouhtml,'返回游戏')

			return gameurl,FLAG

		zhandouhtml=etn(zhandouhtml)
		zhandouurl=fs+'fengshen/'+zhandouhtml.xpath('//body//a/@href')[0]      #需设置默认法术

		zhandouhtml=requests.get(zhandouurl,headers=headers).content

	money=money+int(re.search(r'你获得了胜利。<br>你获得了(.*)枚铜板。',zhandouhtml).group(1))
	experience=experience+int(re.search(r'铜板。<br />.*获得了(.*)点经验。',zhandouhtml).group(1))
	times=times+1

	print u'胜利：'+str(times).decode('utf-8')
	print u'铜板：'+str(money).decode('utf-8')
	print u'经验：'+str(experience).decode('utf-8')
	print u'下次升级经验：'+(re.search(r'下次升级还要(.*)经验',zhandouhtml).group(1)).decode('utf-8')

	zhandouhtml=etn(zhandouhtml)
	gameurl=searchurl(zhandouhtml,'返回游戏')

	return gameurl,FLAG

def jungle(gurl):
	html=requests.get(gurl,headers=headers).content
	url=re.search(r'这里有<a href="(.*)" title=".*</a><br />请选择你的行走方向:',html).group(1)
	gurl=fs+'fengshen/'+url

	html=requests.get(gurl,headers=headers).content
	html=etn(html)
	gurl=fs+'fengshen/'+html.xpath('//body//a/@href')[0]

	html=requests.get(gurl,headers=headers).content
	html=etn(html)
	gurl=searchurl(html,'挑战')

	gurl,FLAG=zhandou(gurl)

	return gurl,FLAG

def etn(html):      #etree化字符串，同时将<br>标签转换为换行符
	html=re.sub('<br>','\n',html)
	html=re.sub('<br />','\n',html)
	html=etree.HTML(html)
	return html

def searchurl(html,st):      #在html中寻找st字符串对应的url
	for a in html.xpath('//body//a'):
		if re.search(st,a.xpath('text()')[0].encode('utf-8')):
			if re.search('/',a.xpath('@href')[0].encode('utf-8')):			#首页进入下层链接
				return fs+a.xpath('@href')[0]
			else:											#其余页面就在首页进入的下层链接的该层进行跳转
				return fs+'fengshen/'+a.xpath('@href')[0]

def main():
	gurl,FLAG=login(play1)
	job(gurl,FLAG)

if __name__ == '__main__':
	main()
