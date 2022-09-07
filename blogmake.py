import datetime
import re
#正規表現で抽出を利用
import os
#ファイル名取得モジュール
import pyperclip as pc 
#クリップボードにコピーするため
s = open('./tex/nowtex/nowtex.tex', 'r', encoding='UTF-8')
data=s.read()
url=re.findall(r'\\url{.*?}',data)
for i in range(len(url)):
	#URLの処遇をどうすればいいのかわからん．a hrefに引き継ぎたいだけなのに...
	url[i]=re.sub(r'\\url{|}','',url[i])
	data=re.sub(r'\\url','url',data)
	print(url[i])
	urlmake=r'url{'+url[i]+'}'
	if urlmake in data:
		print('置換するよ')
		data=re.sub(r'url{.*?}','<a href="'+url[i]+'">URL</a>',data,1)
	#print(data)
category=re.findall(r'\\title{.*}',data)
category[0]=re.sub(r'\\title|{|}','',category[0])
#print(category[0])
title=re.findall(r'\\section{.*}',data)
title[0]=re.sub(r'\\section|{|}','',title[0])
#print(title[0])
article=re.findall(r'\\section{.*}[\s\S]*\\end{document}',data)
body=re.sub(r'\\section{.*}\n|\n*\\end{document}','',article[0])
footnotes=re.findall(r'\\footnote{.*?}',body)
print(footnotes)
footnote=''
for i in range(len(footnotes)):
	footnotes[i]=re.sub(r'\\footnote{|}','',footnotes[i])
	print(footnotes[i])
	body=re.sub(r'\\footnote{.*?}','<sup id="ref_'+str(i+1)+'"><a href="#note_'+str(i+1)+'">'+str(i+1)+')</a></sup>',body,1)#先頭から1回置換にしているのは，re.sub()の置換前に変数を含むと挙動がおかしくなるから．
	footnote=footnote+r'<li id="note_'+str(i+1)+'"><a href="#ref_'+str(i+1)+'">^</a>'+footnotes[i]+'</li>\n'
body=re.sub(r'\n\n',r'\n</p>\n<p>\n',body)
body='<p>\n'+body+'\n</p>'
body=body+'\n<hr>\n<ol class="note">\n'
body=body+footnote+'</ol>'
incategory=''
if category[0]=='impression':
	incategory='個人の感想'
elif category[0]=='study':
	incategory='個人の感想'
elif category[0]=='tech':
	incategory='素人による技術っぽい話'
dt_now = datetime.datetime.now()

subsections=re.findall(r'\\subsection{.*?}',body)
midashi=[]
for i in range(len(subsections)):
	midashi.append(re.sub(r'\\subsection{|}','',subsections[i]))
	body=re.sub(r'<p>\s*?\\subsection{.*?}',r'<h2> <b>＊</b>'+midashi[i]+'</h2><p>',body,1)
print(midashi)
head='<div class="blog-contents wrapper">\n<article>\n<header class="post-info">\n<h2 class="post-title">'+title[0]+'</h2>\n<p class="post-date">'+str(dt_now.month)+'/'+str(dt_now.day)+'<span>'+str(dt_now.year)+'</span></p>\n<p class="post-cat">カテゴリー:'+incategory+'</p>\n</header>\n'
body=head+body
r = open('./tex/template1.html', 'r', encoding='UTF-8')
t = open('./tex/template2.html', 'r', encoding='UTF-8')
temple1=r.read()
temple2=t.read()
body=temple1+body+temple2
print(body)

if(dt_now.month<10):
	month='0'+str(dt_now.month)
else:
	month=str(dt_now.month)
if(dt_now.day<10):
	day='0'+str(dt_now.day)
else:
	day=str(dt_now.day)
if category[0]=='impression':
	u=open('./impression/'+str(dt_now.year)+month+day+'impression.html', 'w', encoding='UTF-8')
elif category[0]=='study':
	u=open('./study/'+str(dt_now.year)+month+day+'study.html', 'w', encoding='UTF-8')
elif category[0]=='tech':
	u=open('./tech/'+str(dt_now.year)+month+day+'tech.html', 'w', encoding='UTF-8')
u.write(body)
u.close()