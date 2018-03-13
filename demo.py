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
import xlwt
from pyquery import PyQuery as pq
import xlsxwriter
from xlrd import open_workbook


type = sys.getfilesystemencoding()

targetUrl = 'http://company.huibo.com/'

loginUrl = targetUrl + 'login'

InterfaceUrl = loginUrl + '/logindo/'

excelFilePath = os.getcwd()  + '\\resume.xlsx'

global keyWord 

keyWord = '前端'

def login() :

    data = {
        'txtUsername' : 'xxxxxxxx',
        'txtPassword' : 'xxxxxxxx',
        'hddseed' : pq( loginUrl )( '#hddseed' ).val(),
        'txtAuthCode' : ''
    }

    headers = {
        'Host' : 'company.huibo.com',
        'Origin' : 'http://company.huibo.com',
        'Referer': 'http://company.huibo.com/login',
        'X-Requested-With' : 'XMLHttpRequest',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
    }

    postData = urllib.urlencode( data )


    cj = cookielib.CookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    request = urllib2.Request( InterfaceUrl , postData , headers )  

    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')]
    
    opener.open( InterfaceUrl , postData )

    op = opener.open( targetUrl )

    result = op.read()

    successLoginName = False

    global cookie

    cookie = ''

    print cj

    for item in cj :

        cookie += item.name + '=' + item.value + '; '

        if( item.name == 'username' ) :

            successLoginName = item.value

    if successLoginName :
        
        print '\n'
        print 'login is success'
        print '----------------------------------------------'

        allPage = 1

        getContent( 1 )

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

        print 'all Page is : ' + str( dataJson[ 'pager' ][ 'total_page' ] )

        allPage = input( 'u need get page number : ' )

        print '-----------------------------------------------------------'

        # allPage = 200

    if nowPage < allPage :

        nowPage += 1

        getContent( nowPage )


global dataBox

dataBox = []

def readData( dataJson ) :

    resumesData = dataJson[ 'resumes' ]

    for index in range(len(resumesData)) :

        item = resumesData[index]

        try :
            # print u'名字：' + item[ 'user_name' ]
            # print u'性别：' + item[ 'sex_text' ]
            # print u'年龄：' + item[ 'age' ]
            # print u'工作年限：' + item[ 'start_work' ]
            # print u'描述：' + item[ 'appraise' ]
            # print u'详细数据地址：http://company.huibo.com/resume/resumeshow/type-network-src-search-resumeid-' + item[ 'resume_id' ]
            # print '------------------------------------------------------------'


            # print item['user_name']

            dataBox.append( item )

            if len(dataBox) == allPage*10 :

                writeData( dataBox )

        except :

            break
            # print u'这个傻逼数据有问题：' + item[ 'user_name' ]
            # print '------------------------------------------------------------'



def writeData( data ) :

    headings = [ u'名字' , u'性别' , u'年龄' , u'工作年限' , u'描述' , u'详细数据地址' ]

    sheetName = keyWord.decode( 'utf-8' )

    workbook = xlsxwriter.Workbook( 'resume.xls' )

    worksheet = workbook.add_worksheet( sheetName )

    worksheet.write_row( 'A1' , headings )

    dataLen = 1

    for index in range(len(data)) :

        rowName = 'A' + str(index+2)

        print rowName

        worksheet.write_row( rowName , [ 
            data[index]['user_name'] ,
            data[index]['sex_text'] ,
            data[index]['age'] ,
            data[index]['start_work'] ,
            data[index]['appraise'] ,
            'http://company.huibo.com/resume/resumeshow/type-network-src-search-resumeid-' + data[index]['resume_id'] ,
        ])




login()








