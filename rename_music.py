import os
import os.path
import re
import urllib.request
import time

#todo:过滤文件中的英文:
#修改url，com/#/song就可以了

def rename_file():
    path = '.'
    for parent,dirnames,filenames in os.walk(path):
        #print(filenames)
        for filename in filenames:
            o_path = path + '/' + filename
            song_id = get_song_id(filename)
            #print(song_id)
            if song_id == None:
                continue
            song_info = get_song_info(song_id)
            
            #print(song_info)
            itr = 0
            for itr in range(2):
               song_info[itr] = translate_code(song_info[itr])
            #print(song_info)
            if len(song_info[0]) > 20:
                song_info[0]=song_info[0][0:20]
            if len(song_info[1]) > 20:
                song_info[1]=song_info[1][0:20]
               
            n_filename = song_info[0]+'-'+song_info[1]+'.uc'
            n_path = path + '/' + n_filename
            os.rename(o_path,n_path)
            #print(filename+' rename-> '+n_filename+'\n'+'o_path:'+o_path+'\n n_path:'+n_path)
            print(filename+' rename-> '+n_filename+'\n')
            time.sleep(15)


def get_song_id(filename):
    #正则提取文件名中的id
    exp = '(\d+)-\d+-\w+.uc'
    match = re.search(exp,filename)
    #print(match.group(),match.group(1))
    if match == None:
        return None
    else:
        return match.group(1)

def get_song_info(id):
    get_url = 'https://music.163.com/song?id='+id
    context = get_song_web_context(get_url)

    #正则提取网页中的title元素
    
    exp = '<title>([\s\S]+) - ([\s\S]+) - \S+ - \S+</title>'
    #context = '<head> <meta charset="utf-8"><meta name="baidu_ssp_verify" content="39f14c78c537175eb4b5192c72d002c1"><meta name="baidu-site-verification" content="cNhJHKEzsD"><meta name="360-site-verification" content="e37aef53e3922913e2a6a4682e479b84"><meta name="sogou_site_verification" content="7zFjYjJaMq"><meta name="msvalidate.01" content="0CA3171633345524D8CBED5E95C75FFF"><meta name="google-site-verification" content="rh2irYN2Lu028orAseOD3aXd5u7Eu1mqTfhoVaw2Ihg"><meta name="shenma-site-verification" content="12da4afc02bfe908ed0667f287167d11_1555581349"><meta property="qc:admins" content="27354635321361636375"><link rel="canonical" href="https://music.163.com/"><meta name="applicable-device" content="pc,mobile"><title>完 - 陈奕迅 - 单曲 - 网易云音乐</title><meta name="keywords" content="网易云音乐，音乐，播放器，网易，下载，播放，DJ，免费，明星，精选，歌单，识别音乐，收藏，分享音乐，音乐互动，高音质，320K，音乐社交，官网，music.163.com"><meta name="description" content="网易云音乐是一款专注于发现与分享的音乐产品，依托专业音乐人、DJ、好友推荐及社交功能，为用户打造全新的音乐生活。"><meta property="og:title" content="网易云音乐"><meta property="og:type" content="website"><meta property="og:image" content="http://p3.music.126.net/tBTNafgjNnTL1KlZMt7lVA==/18885211718935735.jpg"><meta property="og:url" content="https://music.163.com/"><meta property="og:site_name" content="网易云音乐"></head>' 
    match = re.search(exp,context)
    if match == None:
        print('first time catch nothing,try second')
        get_url = 'https://music.163.com/#/song?id='+id
        context = get_song_web_context(get_url)
        match = re.search(exp,context)
        print(match.group())
    #print(match.group(),match.group(1),match.group(2))
    #print(context)
    return [match.group(1),match.group(2)]

def get_song_web_context(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    context = response.read().decode('utf-8')
    #print(context)
    return context

#把/转成_
def translate_code(str):
    exp = '/'
    match = re.search(exp,str)
    if match !=None:
        def replace(matchobj):
            if matchobj.group(0) == '/':
                return '_'
        str = re.sub(exp,replace,str)
    return str




rename_file()
#title = '<title>天下无敌（inspired by movie “赌神”） - 卢冠廷 - 单曲 - 网易云音乐</title>'
#title = '<title>情人 (live) - 张学友 - 单曲 - 网易云音乐</title>'
#exp = '<title>([\s\S]+) - ([\S\s]+) - \S+ - \S+</title>'
#match = re.search(exp,title)
#print(match.group()+'\n'+match.group(1)+'\n'+match.group(2)+'\n')
#info = ['十年(Live)', '韩红']
#exp = '\S+(/)\S+'


