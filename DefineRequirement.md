

# 需求设定 #
  * 属主: 张沈鹏
  * 读者: 所有对 mailgroup 项目有兴趣的开发者

本着产品开发从最小功能集做起的方式,我们先定义一个最小的需求集， 以便于开始开发
  * 此外 ，我们可以把设计作为文档
  * 在完成一个最基本的雏形以后在python 的 maillist中发布 ， 同时让跟多的人参与进来
  * 一期工程不需要任何界面 只需要提供api

> 下面是我提议的方案::
    * 大家可以看看是否有细节需要调整 然后给出具体的表设计和函数接口设计
    * ZoomQuiet ~ 没有见到回复邮件时,线索ID 的设定?!
      * 就象真实的 mailing list 通过 message id 的值,进行父子关系的层级处置的...

## 表结构 ##
首先定义涉及到表结构， 也是最小的功能集， 越精简越好

### 数据表 ###
  * mailgroups 邮件群
    * id
    * gname 群的英文名
  * mg\_user 用户
    * id
    * signature 用户的签名
    * mailbox 用户的邮箱
  * mail 邮件
    * id
    * topicid 主题id
    * title
    * body
    * type 格式 （html / text）
    * create\_time
    * usrid 用户id
    * mgrid 群id
    * status 状态 （待审批、被拒绝 、 待群发、已经群发） //一期工程只需要后两个状态
  * topic 主题
    * id
    * topic       主题名(UNIX格式)
    * +`topic_desc  主题描述`
    * mgrid 群id


### 关系表 ###
  * 群-用户
    * 群id
    * 用户id
    * 订阅状态

## 操作 ##
（每个操作对应一个url的api）

  * 群
    * 创建群
    * 绑定用户
    * 删除用户
  * 用户
    * 创建用户
    * 更新用户签名档
  * 邮件
    * 发送邮件(新建主题)
    * 回复(某楼的邮件)

> api::
    * 设计风格可以参考新浪微博
    * 不过我们不需要搞复杂的权限验证 用MD5+API\_KEY计算一个签名就可以了
      * ZoomQuiet ~ 建议包含时间戳,以便进行有效性,或是时间线的核查

# 参考 #
  * [RFC 5322](http://datatracker.ietf.org/doc/rfc5322/?include_text=1)Internet Message Format(2008/10 已经有勘误)
  * [RFC 821](http://www.rfc-editor.org/info/rfc821)简单邮件传输协议(SMTP)(已经废弃)
  * [RFC 822](http://www.rfc-editor.org/info/rfc822)联网文本信息格式(信头格式)
  * [RFC 974](http://www.rfc-editor.org/info/rfc974)邮件路由和域系统(MX路由)
  * [RFC 1344](http://www.rfc-editor.org/info/rfc1344)MIME对互联网邮件网关的意义
  * [RFC 1892](http://www.rfc-editor.org/info/rfc1892)用于报告邮件系统管理信息的多部分/报告内容类型
  * [RFC 2045](http://www.rfc-editor.org/info/rfc2045)多用途互联网邮件扩展(MIME)第一部分：互联网信息正文格式 Updated by RFC 2231
  * [RFC 2046](http://www.rfc-editor.org/info/rfc2046)多用途互联网邮件扩展(MIME)第二部分：媒介类型
  * [RFC 2047](http://www.rfc-editor.org/info/rfc2047)多用途互联网邮件扩展(MIME)第三部分：非ASCII文本信息头扩展 Updated by RFC 2231
  * [RFC 2048](http://www.rfc-editor.org/info/rfc2048)多用途互联网邮件扩展(MIME)第四部分：注册过程
  * [RFC 2369](http://www.rfc-editor.org/info/rfc2369)邮件列表头信息的显示
  * ...