

# 邮件展示 #
  * 目标:追求合适,统一的展示效果
  * 障碍:各种邮件客户端所支持的标准不同,第一期只考虑gmail
  * 捷径?考察google groups 邮件在gmail中的展示效果.
```
邮件展示可以分为txt和html两个形式
txt是基础,各种状况下都支持.
html和css在各种邮件客户端情况下支持有所不同.
```
    * ZoomQUiet ~ 建议:
      1. 目前就支持 text 格式
      1. 目前就支持 utf-8 编码信息,也不尝试进行兼容性转换
      1. 参考 googlegroups 的綫索界面,将一个主題线索的回复,使用层级的形式进行精确的展示
        * 可以使用 AJAX 效果,进行自动折叠
        * 最好配合有键盘操作,可以快速打开对应回复来查阅
        * 快捷键,同 gmail 的设定最好
      1. 在标准的邮件缀文中,自动给出 42区相关`邮件组`和分类标签的链接

# 参考 #
  1. [wiki:HTML\_e-mail](http://en.wikipedia.org/wiki/HTML_e-mail)
  1. [Guide to CSS support in email clients](http://www.campaignmonitor.com/css/)