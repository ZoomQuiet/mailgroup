42qu:找到给你答案的人



# 结合42qu基于GAE的邮件组系统 #

## 目前存在的问题 ##

  1. 大家不能天天挂在网上面，没时间刷网页,比较忙的人不能从BBS/QQ群之类的地方获取信息.
  1. 大家讨论的时候互相不知道真实身份,导致网络交流不负责任.
  1. 小组讨论的人群没有区分度,小白乱发言,让高手厌烦.(习惯BBS/QQ群的小白,就算进入列表,也没有对自个儿发言负责的自觉)
  1. 中国没有好的邮件列表，既能通过邮箱件方式讨论，又能通过网页方式讨论.（google groups不错，但被墙掉了）
  1. 缺乏一个讨论被整理出来成为知识的手段。讨论-》信息-》知识

### 42qu功能相关 ###
  1. 人们在找工作的时候,希望了解公司是什么文化,将要和什么样的人工作,同事都做过什么.但是先在这些信息没有较好的展示.
  1. 对社区的贡献应该成为个人简历的一部分，也方便被用人企业发现,42qu可以成为相互展示和发现的平台.
    * 同质的有 http://gurudigger.com/ 等,针对专门领域的开源贡献进行了自动挖掘,也可考虑整合

## 邮件相关需求 ##
一个邮件组系统,简单的理解为一个基于邮件的BBS系统:
```
基本管理事务::
    创建邮件组
    删除邮件组
    更改邮件组介绍信息
    添加邮件组成员
    删除邮件租成员
    屏蔽邮件租成员

基础交流行为::
    发布话题
    回复话题

扩散到42区::
    邮件内容的展示.
    邮件组成员的实名制,个人资料链接到42qu.
    讨论信息

知识管理深入::
    讨论转化为信息(技术实现?)
    信息转化为知识(众包?)
```

  * ZoomQuiet ~ 进一步要澄清的:
    1. `邮件组` 和 googlegroups 这种 邮件列表服务有什么不同/关系?
    1. `话题`在 42qu 中的定位? 和 邮件列表中的主题 有什么不同/关系?
    1. `讨论`/`信息`/`知识` 三者在 mailgroup 中的定位/关联/转化?

![https://wiki.mailgroup.googlecode.com/hg/mindmap/mailgroup_elements_idx.png](https://wiki.mailgroup.googlecode.com/hg/mindmap/mailgroup_elements_idx.png)
  * 图谱源代码: [mailgroup\_elements\_idx.dot](https://wiki.mailgroup.googlecode.com/hg/mindmap/mailgroup_elements_idx.dot)
  * 以上是 ZoomQuiet 的设想:
    1. 42区的邮件组包含领域主题和对应的回复,以及回复的回复
    1. googlrgroups 使用传统的模式,包含由主题引发的线索以及对应的回复
    1. 通过 mailgroup 进行有选择的:
      * 主题邮件和笔记 的相互复制
      * 对应回复的邮件和笔记评注的相互抄纳
    1. 进一步的,在 42区中,用简单的维基,进行知识点的聚合/整理


## web需求 ##
  1. 邮件组相关信息的浏览
  1. 参与讨论

## 长远目标 ##
成为一个很多人可以参加的开源项目.会有api,开放平台.企业可以用它减小成本.

将需求列出来,明码标价,让大家参与.发展中国可持续的开源环境.

提高工程师话语权(facebook的工程师文化)

## 项目特性 ##
这是一个开源项目,为了让中国的其他团体也能用上靠谱的开源资源,减小企业成本.

  * 本开源项目是有报酬的,目前由42qu赞助.`大家一定要收钱!(不收钱会提高的开源道德门槛,不利于让更多的人参与进来)`
  * 当基础功能和框架完成后,将功能需求发布出来明码标价.最好能让在校大学生完成,这些经历也能写入他们的42qu资料中,能成为他们找工作的筹码.用人单位也方便在他们中招人.
    * ZoomQuiet ~ 这是改变一个行业习惯心理行为的开始哪! 回归用纯粹的智力成果来获得报酬的史前黄金时代!



