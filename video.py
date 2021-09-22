#-*- coding:utf-8 -*-

import os

url = 'https://video-website-demo.com'

class VideoInfo: #可同时下载多个视频
    video = [
        '/VirtualPath1',  #视频1
        '/VirtualPath2',  #视频2
        '/VirtualPath2'   #视频3
    ]

try:
    import requests
except ImportError:
    raise SystemExit('\n[!] requests import error!,use pip install requests to install!')

try:

    print 'TS Video Download\n'
    
    for index in range( len( VideoInfo.path ) ):
        print 'Downloading video' + str(index+1)
        
        vurl = url + VideoInfo.path[index]
        vurl += '@@hd-' #画质参数，根据实际的 URL 中有没有这个参数来选择加或不加
        
        s = requests.Session()

        maxcount = 500 #TS片段编号上限，根据视频内容不同，编号上限会不一样，需要根据实际情况进行调整
        
        for i in range(1, maxcount): 
            
            r = s.get( vurl + str(i).zfill(5) + '.ts' )
            print 'Downloading ' + vurl + str(i).zfill(5) + '.ts' + ' size ' + str(len(r.content)) + ' byte'
            
            if len(r.content) < 1024:
                print 'files < 1kb have been ignored\n'
                break
            
            file_object = open( str(i).zfill(3) + '.ts', 'wb' ) #设定位宽，以免拼接时发生错误，位宽长度需要与片段编号匹配
            file_object.write(r.content)
            file_object.close()
        
        os.popen( 'copy /b  ???.ts  video' + str(index+1) + '.ts' ).readlines() #注意通配符，通配符长度需要与片段编号匹配
        
        for fileindex in range( 1, maxcount ): #清理工作
            FullPath = os.path.join( os.getcwd(), str(fileindex).zfill(3) + '.ts' )
            if os.path.exists(FullPath):
                os.remove(FullPath)
            else:
                break

except KeyboardInterrupt:
    raise SystemExit('exit!')
