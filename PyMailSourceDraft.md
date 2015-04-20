


# Python邮件相关 #
ZoomQuiet 大妈写的文档非常好,以至于给我很大的压力让我难以下笔.
  * 因此我希望在我求助之前能自己来改进含有 _Draft的文档和代码.高手们只要指出我的错误和不妥的地方,以及做得好的地方就可以了.具体的过程还是让我这只菜鸟多实践吧.
    * ZoomQuiet ~ 首先将维基修订为 WikiName 格式的命名了,以便引用; 另外要进行统一的 `Draft` 标识,可以使用 标签
    * 即,在维基头部使用 `#labels Draft` 这种声明_

## 内置模块 ##
Python 文档标准库的第18章有相当多涉及到mail的资源.
[18. Internet Data Handling](http://docs.python.org/library/netdata.html)
  * 18.1. email — An email and MIME handling package
  * 18.2. json — JSON encoder and decoder
  * 18.3. mailcap — Mailcap file handling
  * 18.4. mailbox — Manipulate mailboxes in various formats
  * 18.5. mhlib — Access to MH mailboxes
  * 18.6. mimetools — Tools for parsing MIME messages
  * 18.7. mimetypes — Map filenames to MIME types
  * 18.8. MimeWriter — Generic MIME file writer
  * 18.9. mimify — MIME processing of mail messages
  * 18.10. multifile — Support for files containing distinct parts
  * 18.11. rfc822 — Parse RFC 2822 mail headers
  * 18.12. base64 — RFC 3548: Base16, Base32, Base64 Data Encodings
  * 18.13. binhex — Encode and decode binhex4 files
  * 18.14. binascii — Convert between binary and ASCII
  * 18.15. quopri — Encode and decode MIME quoted-printable data

GAE源码中:google/appengine/api/mail.py 的源码是gae处理mail的主要资源.

## 决策 ##
在大该略读相关文档后,发现python已经把mail的处理支持得相当好了,我们弄懂使用好了就行.
设想的工作过程(之间过程应该多次迭代):
  1. 制作出虚拟的目标邮件用例
  1. 根据目标邮件用例生成源码
  1. 在源码中插入系统标记
  1. 发送插入系统标记后的目标邮件用例,检验在各个邮件接收终端中的展示情况
  1. 根据系统关键字规则和邮件发送流程编写mailgroup系统.
  1. 测试效果
  1. 一期交付

邮件接收端可以看邮件源码:
  * 如:Thunderbird 选中邮件,按 View 菜单 Message Source

MIME(Multipurpose Internet Mail Extensions)是邮件处理的基础的关键:推荐资料
  * Multipurpose Internet Mail Extensions
  * 系统关键字就可以通过mime x-或者X-开头的标记定义处理
