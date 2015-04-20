

# 42qu.com 接口 #
用于与42区通讯


## 格式 ##
人物反查接口
```
URL请求:
http://api.42qu.com/search/man/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*
(别被吓到了,后面就一电子邮件地址)
返回:
{
"appearance_fee":          #出场费
"ico":                     #头像
"uid":                     #用户名
"title":                   #标题
"company":                 #公司
"about_me":                #关于我
"signature":               #签名
"link":[                   #链接
["新浪微薄": ],
["豆瓣": ],
["Buzz": ],   
["Twitter": ],       
["LinkedIn": ],
["SlideShare": ],
["网易微薄": ],
       ...
]
"id":                      #用户id
"name":                    #姓名
}
```

## 示例 ##
```
人物资料反查接口
URL请求:
http://api.42qu.com/search/man/silegon@gmail.com
返回:
{"appearance_fee":0.41999999999999998
    ,"ico":"http://i.42qu.net/pic_show/219/33/99/16692.jpg"
    ,"uid":"silegon"
    ,"title":"python web \u5f00\u53d1"
    ,"company":"99fang"
    ,"about_me":"\u975e\u5b98\u65b9\u6d3b\u52a8\u7ec4\u7ec7\uff0c\u793e\u56e2\u6587\u5316\u89c4\u5212\u3002"
    ,"signature":"\u76f4\u9762\u73b0\u5b9e"
    \,"link":[["\u8c46\u74e3","http://www.douban.com/people/forpm/"]
        ,["Blog","http://forpm.net"]]
    ,"id":10016494,"name":"\u5468\u51ef\u534e"}

URL请求:
http://api.42qu.com/search/man/zsp007@gmail.com
返回:
{"appearance_fee":42
    ,"ico":"http://i.42qu.net/pic_show/219/27/69/6311.jpg"
    ,"uid":"zuroc"
    ,"title":"\u521b\u59cb\u4eba&\u7a0b\u5e8f\u5458"
    ,"company":"42qu.com"
    ,"about_me":"HTML, CSS, Javascript, Linux, Python, \u6570\u636e\u6316\u6398,\u7f51\u7ad9\u67b6\u6784 ...\r\n\u4ec0\u4e48\u90fd\u7565\u61c2\u4e00\u70b9\u3002\r\n\u5982\u679c\u5bf9\u6211\u7684\u7f51\u7ad9\u611f\u5174\u8da3, \u4e5f\u6b22\u8fce\u8054\u7cfb\u6211\u3002"
    ,"signature":"\u5929\u624d = 1%\u7684\u7075\u611f + 99%\u7684\u6c57\u6c34"
    ,"link":[["\u8c46\u74e3"
        ,"http://www.douban.com/people/zuroc/"]
        ,["Buzz","https://www.google.com/profiles/zsp007"]
        ,["Blog","http://zsp.javaeye.com/"]]
    ,"id":10000000,"name":"\u5f20\u6c88\u9e4f"}

```