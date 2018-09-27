from lxml import etree
import urllib.request
import os
import socket
import time

headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.4793.400 QQBrowser/10.0.743.400")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
#将opener安装为全局
urllib.request.install_opener(opener)
timeout = 20
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
sleep_download_time = 10
time.sleep(sleep_download_time) #这里时间自己设定

#获取每页的网页链接
def getlink(url):
    file=urllib.request.urlopen(url)
    data=str(file.read())
    data=etree.HTML(data)
    html_data=data.xpath('//div/a[@class="movie-box"]//@href')
    link=list(set(html_data))
    return link

def picture(url):
    html1=urllib.request.urlopen(url).read()
    html1=str(html1)
    html1 = etree.HTML(html1)
    mainpicture = html1.xpath('//div/a[@class="bigImage"]/img//@src')
    subpictures=html1.xpath('//div/a[@class="sample-box"]//@href')
    wholepictures=mainpicture+subpictures
    return wholepictures

#将网络图片保存至本地
def save_picture(img_url,file_name,file_path):
     x=1
     for img_ur in img_url:
         try:
             # 是否有这个路径
             if not os.path.exists(file_path):
                 # 创建路径
                 os.makedirs(file_path)
                 # 获得图片后缀
             file_suffix = os.path.splitext(img_ur)[1]
             print(file_suffix)
             # 拼接图片名（包含路径）
             filename = '{}{}{}{}{}'.format(file_path, os.sep, file_name,str(x), file_suffix)
             print(filename)
             # 下载图片，并保存到文件夹中
             urllib.request.urlretrieve(''.join(img_ur), filename=filename)

         except IOError as e:
             print("IOError")
             x+=1
         except Exception as e:
             print("Exception")
             x+=1
         x+=1

for x in range(1,10):
    url="https://www.seedmm.net/"+"page/"+str(x)
    #得到每一页的作品链接
    links=getlink(url)
    print(links)
    for link in links:
        fanhao = link.split('/')[-1]
        picture_links = picture(link)
        print(picture_links)
        save_picture(picture_links,file_name=fanhao,file_path='E:/tupian')


