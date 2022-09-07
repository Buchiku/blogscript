import datetime
import re
#正規表現で抽出を利用
import os
#ファイル名取得モジュール
import pyperclip as pc 
#クリップボードにコピーするため
ti=[]
date=[[]]
title=[]
category=[]
alldata=[]
path=['impression','tech','study']

for i in range(len(path)):
	files = os.listdir(path[i])
	files_file = [f for f in files if os.path.isfile(os.path.join('./'+path[i], f))]
	for j in range(len(files_file)):
		now=files_file[j]
		t=[]
		year=re.findall(r'^\d\d\d\d',now)
		now=re.sub(r'^\d\d\d\d','',now)
		month=re.findall(r'^\d\d',now)
		now=re.sub(r'^\d\d','',now)
		day=re.findall(r'^\d\d',now)
		now=re.sub(r'^\d\d','',now)
		date.append([year[0],month[0],day[0]])
		x=year[0]+month[0]+day[0]
		time=datetime.datetime.strptime(x,'%Y%m%d')
		#print(time)
		ti.append(time)
		now=re.sub(r'\.html','',now)
		category.append(now)
		s=open('./'+now+'/'+files_file[j],encoding="utf-8")
		contents=s.read()
		cont=re.findall(r'<h2 class="post-title">.*</h2>',contents)
		s.close()
		cont[0]=re.sub(r'<.*?>','',cont[0])
		#print(cont[0])
		title.append(cont[0])
	#print(files_file)
date.pop(0)
#print(date)
#print(category)
#print(title)
#print(ti)
alldata=[ti,date,category,title]
#print(alldata)
alldata=[list(x) for x in zip(*alldata)]
alldata=sorted(alldata, reverse=True, key=lambda x: x[0])#リスト内包表記で行列を転地している．タプルで出力されるのを防ぐためらしい．
#print(alldata)
text='<div class="blog-contents wrapper">\n<article>'
for i in range(len(alldata)):
	text=text+'<header class="post-info">\n<h2 class="post-title"><a href="'+alldata[i][2]+'/'+alldata[i][1][0]+alldata[i][1][1]+alldata[i][1][2]+alldata[i][2]+'.html">'+alldata[i][3]+'</a></h2>\n<p class="post-date">'+alldata[i][1][1]+'/'+alldata[i][1][2]+'<span>'+alldata[i][1][0]+'</span></p>\n<p class="post-cat">カテゴリー:'
	if alldata[i][2]=='study':
		text=text+'勉強したこと</p>\n</header>\n'
	elif alldata[i][2]=='tech':
		text=text+'素人による技術っぽい話</p>\n</header>\n'
	elif alldata[i][2]=='impression':
		text=text+'個人の感想</p>\n</header>\n'
#print(text)

a=open('./tex/template1.html','r',encoding='UTF-8')
b=open('./tex/template2.html','r',encoding='UTF-8')
c=open('./blog.html','w',encoding='UTF-8')
a=a.read()
b=b.read()
index=re.sub(r'\.\.',r'.',a+text+b)
c.write(index)
c.close()
for i in path:
	li=re.findall(r'<header class="post-info">\s*<h2 class="post-title"><a href="'+i+'.*?</a></h2>\s*<p class="post-date">.*?</p>\s*<p class="post-cat">カテゴリー:.*?</p>\s*</header>',index)
	output=a+'<div class="blog-contents wrapper">\n<article>'
	for j in range(len(li)):
		output=output+li[j]+'\n'
	output=output+b
	output=re.sub(r'\.\.','.',output)
	end=open('./blog'+i+'.html','w',encoding='UTF-8')
	end.write(output)
	end.close()
	print(li)