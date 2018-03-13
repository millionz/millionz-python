# -*- coding: utf-8 -*-

import urllib
import re
import os
import json
import sys
import urllib2  
import cookielib  
import string  
import re 
from pyquery import PyQuery as pq

type = sys.getfilesystemencoding()

targetUrl = 'http://company.huibo.com/'

loginUrl = targetUrl + 'login'

InterfaceUrl = loginUrl + '/logindo/'

global keyWord 

keyWord = '前端'

def login() :

    data = {
        'txtUsername' : 'pachongkeji',
        'txtPassword' : 'pachongkeji123',
        'hddseed' : pq( loginUrl )( '#hddseed' ).val(),
        'txtAuthCode' : ''
    }

    headers = {
        'Host' : 'company.huibo.com',
        'Origin' : 'http://company.huibo.com',
        'Referer': 'http://company.huibo.com/login',
        'X-Requested-With' : 'XMLHttpRequest',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    postData = urllib.urlencode( data )

    cj = cookielib.CookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    request = urllib2.Request( InterfaceUrl , postData , headers )  

    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    
    opener.open( InterfaceUrl , postData )

    op = opener.open( targetUrl )

    result = op.read()

    successLoginName = False

    global cookie

    cookie = ''

    for item in cj :
        cookie += item.name + '=' + item.value + '; '
        if( item.name == 'username' ) :
            successLoginName = item.value

    if successLoginName :
        
        print '\n'
        print 'login is success'
        print '----------------------------------------------'

        

        allPage = 1

        getContent( 1  )

    else :
        print 'login is error'
        exit()


def getContent( page ) :

    global nowPage

    nowPage = page


    searchUrl =  'http://company.huibo.com/resumesearchnew/search?&ct=1&st=1&k='+ keyWord +'&s=0&ma=0&so=1&ps=20&p='+ str(page) +'&tt=0'

    headers = {
        'Host' : 'company.huibo.com',
        'Referer': 'http://company.huibo.com/resumesearchnew/',
        'X-Requested-With' : 'XMLHttpRequest',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Cookie' : cookie
    }

    req = urllib2.Request( searchUrl ,headers=headers )

    res = urllib2.urlopen( req )

    # response  = urllib.urlopen( requestData )

    dataJsonStr =  str( res.read() )

    dataJson = json.loads( dataJsonStr )

    readData( dataJson )

    if page <= 1 :

        global allPage

        allPage = int( dataJson[ 'pager' ][ 'total_page' ] )

    if nowPage < allPage :

        nowPage += 1

        getContent( nowPage )


def readData( dataJson ) :

    resumesData = dataJson[ 'resumes' ]

    for index in range(len(resumesData)) :

        item = resumesData[index]
        try :
            print u'名字：' + item[ 'user_name' ]
            print u'性别：' + item[ 'sex_text' ]
            print u'年龄：' + item[ 'age' ]
            print u'工作年限：' + item[ 'start_work' ]
            print u'描述：' + item[ 'appraise' ]
            print u'详细数据地址：http://company.huibo.com/resume/resumeshow/type-network-src-search-resumeid-' + item[ 'resume_id' ]
            print '------------------------------------------------------------'
        except :
            print u'这个傻逼数据有问题：' + item[ 'user_name' ]
            print '------------------------------------------------------------'



login()












