# -*- coding: utf-8 -*-

import urllib
import re
import os
import json
import sys
type = sys.getfilesystemencoding()


# 加载指定url的html
def getHtml( url ) :
    page = urllib.urlopen( url )
    html = page.read()
    return html


# 根据页码获取接口地址
def getUrl( page ) :
    return 'https://mainsite-restapi.ele.me/shopping/restaurants?extras%5B%5D=activities&geohash=ws1030hcb8b&latitude=22.54425&limit=24&longitude=113.95674&offset='+ str( page * 24 ) +'&terminal=web'


# 正则匹配html里的图片地址下载到本地
def getImg( html ) :
    # 加载过来的html转码，不然中文会乱码
    html = html.decode('utf-8').encode(type)
    print '\n'
    # 先匹配src地址，再匹配名字，src地址和名字下标相同
    imgReg = "(?:\"image_path\":\")([^\"]+)"
    imgRe = re.compile( imgReg )
    imglist = re.findall( imgRe , html )
    nameReg = "(?:\"max_applied_quantity_per_order\":-1,)(\"name\":\")([^,\"next_business_time]+)"
    nameRe = re.compile( nameReg )
    nameList = re.findall( nameRe , html )
    if len( imglist ) > 0 :
        if os.path.exists( os.getcwd() + '\img' ) != True :
            os.mkdir( 'img' )
        for index in range(len(imglist)) :
            imgurl = imglist[index]
            if re.search( r'jpeg' , imgurl ) :
                url =  re.compile( r'jpeg' ).sub( 'jpeg.jpeg' , imgurl )
            elif( re.search( r'png' , imgurl ) ) :
                url =  re.compile( r'png' ).sub( 'png.png' , imgurl )
            url = 'https://fuss10.elemecdn.com/' + imgurl[0:1] + '/' + imgurl[1:3] + '/' + url[3:-1] +'g' 
            try :
                name =  nameList[index][1].strip()
            except :
                print nameList
                name = str(imgurl)
            try :
                # 下载到指定目录，并重命名，s%为需要替换名字的地方
                urllib.urlretrieve( url , 'img/%s.jpg' % name )
                print  'success : ' + url + '\n'
            except IOError:
                print '>>> error : ' + url + '\n'


def init() :
    page = 0
    maxPage = 41
    # 看了下数据大概有41页，所以这里做了个循环
    while ( page < maxPage ) :
        page += 1
        html = getHtml( getUrl( page ) )
        print '----------------- start load No.' + str( page ) + ' Data , Index = '+ str(page*24) +'-------------'
        getImg( html )
    print '>>> is End <<<'

init()