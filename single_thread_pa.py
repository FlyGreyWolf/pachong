import requests
import re

#伪装请求头
headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWe"
                  "bKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36", #伪装成浏览器访问
    "referer": "https://www.mzitu.com/all/" #破解网站的防盗链
}

url_init = "https://www.mzitu.com/all/" #初始爬虫页面
pic = "<li>.*?<img.*?data-original='(.*?)'.*?</li>" #匹配html页面中的图片链接，返回(.*?)括号内的内容，即匹配到的html页面中的图片链接
links = '<a href="(.*?)".*?'    #匹配html页面中的跳转链接，返回(.*?)括号内的内容，即匹配到的html页面中的跳转链接

index = 0   #图片命名，自增,1.jpg 2.jpg ....
hashmap = {}    #存储已经访问过的html链接{url1:1,url2:1,....,url_n:1}

#开始爬虫
def start_pa(url):
    
    global index    #引用外部index变量
    global hashmap  #引用外部hashma爬变量

    response = requests.get(url, headers=headers)   #请求url
    html = response.text    #返回结果，一个html
    hashmap.update(url=1)  #记录该链接，表示已经访问过了
    pic_src = re.findall(pic, html) #找到html中所有的图片链接
    html_link = re.findall(links, html) #找到html中所有的跳转链接

    #遍历html中的图片链接
    for src in pic_src:
        index += 1
        r = requests.get(src, headers=headers)  #请求图片链接，返回结果
        with open(str(index) + '.jpg', 'wb') as f:
            f.write(r.content)  #二进制方式写图片二进制码，存储图片
        print("download---"+str(index)+".jpg")
    
    #遍历当前html中的跳转链接
    for link in html_link:
        if not(link in hashmap.keys()): #若没访问过
            start_pa(link)  #就继续爬该没访问过的链接


if __name__ == '__main__':
    start_pa(url_init)


