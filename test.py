#coding=utf-8

import requests
import re
from lxml import etree
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

play1='http://www.mfengshen.com/wapgame.php?sid=a630553b1827c84c16e9a48d4ae2625e'

html=requests.get(play1).content
html=re.sub('<br>','\n',html)

html=etree.HTML(html)

html = html.xpath('string(//body)').encode('utf-8')

print html

jz='你好你好你好11111111111111111111111111111111111111'
print jz.decode('utf-8')

start=time.time()
time.sleep(1)
print '00000000000000000'+time.time()-start

a='123'

def h():
    print a
    hh()
    print a,a,a

def hh():
    global a
    a='321'
    print a,a

h()

print a,a,a,a

s='''
<a>333
    <a>222
        <c>111</c>
    </a>
</a>'''

s=etree.HTML(s)
print s.xpath('//text()')
print s.xpath('a/text()')

x=1
y=5
while x<y:
    x=x+3
    y=y+1

print x,y

a='520'
print int(a)+1

def aaa():
    return 52511,946

a,b=aaa()
print a
print b

if 0<2<3:
    print '111'

ss='abbcccddddeeeddddeeffffff'
if not re.search('a',ss):
    print '55555555555555555555555555555555555555555'


print re.search(r'(dddd){1}(.*)f{3}',ss).group(2)
if re.search(r'd{2}.*f{3}',ss):
    print 'Yes'
else:
    print 'No'

s=[]
for a in s:
    print s
a=1
if a==1:
    print a

import time

print '111111'
time.sleep(1)
print '222222'
time.sleep(1)
print '333333'
