## 介绍
用Java开发的基于restful web接口的搜索服务器，是一个分布式的搜索引擎。

**ELK**，一个分布式的日志分析系统，基于elasticsearch,logstash,kibana。

* 传统关系数据库的缺点
1. 无法打分（给结果根据打分后排序）
2. 无分布式
3. 无法解析搜索请求（我想学Python）
4. 效率低
5. 分词

nosql相比于rdb可以存储丰富形式的数据，如mysql设计表的第一范式要求字段不能含有数组类型的值，而mongodb可以直接按json格式存下来。
elasticsearch可以看做一个nosql，但是update比mongodb慢很多，主要用于搜索。

## 安装
1. 安装Java，需要SDK在8以上版本。
2. 安装[elasticsearch-rtf](https://github.com/medcl/elasticsearch-rtf)，国内大神集成了很多插件的版本
3. 安装[head插件](https://github.com/mobz/elasticsearch-head)，相当于navicat之于mysql，提供web可视化功能
4. 安装[kibana](https://www.elastic.co/cn/downloads/kibana)，需要注意的是要安装与rtf对应的版本。这是主要进行rest操作的工具。
**注意** 安装好head插件后，可能并不能访问9200端口的elasticsearch，需要在elasticsearch-rtf的config文件夹下的yml文件中配置相应的安全策略，将下面的代码保存在yml文件最后。
```
http.cors.enabled: true
http.cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS. HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Length, X-User"
```
## 相关概念
1. 集群：一个或多个节点组织在一起
2. 节点：一个节点是集群中的一个服务器，由一个名字来标识，默认是一个随机漫画角色的名字
3. 分片：将索引划分为多份的能力，允许水平分割和扩展容量，多个分片响应请求，提高性能和吞吐量
4. 副本：创建分片的一份或多份的能力，一个节点失败其余节点可以顶上
elasticsearch和mysql中一些基本概念的对应

elasticsearch|mysql
-|-
index(索引)|数据库
type(类型)|表
documents(文档)|行
fields|列

**倒排索引**
目前搜索引擎的底层存储都采用倒排索引，这也是elasticsearch区别于其他数据库的核心。与TF-IDF(词频-逆文档频率指数，某个词重要性越高，其TF-IDF值就越大)关系密切。

倒排索引源于实际中需要根据属性值来查找记录。这种索引表中每一项都包括一个属性值和具有该属性值的各记录的地址。由于不是由记录来确定属性值，而是由属性值来确定记录的位置，因而成为倒排索引。带有倒排索引的文件成为倒排索引文件，即倒排文件。

文章|内容
-|-
文章A|python django python
文章B|ruby和python两种语言
文章C|学习python PHP和django

在上述3个文章中查询含有python字符的文件，如果不采用倒排索引，就需要逐个遍历查询，如果文章数量大则效率极低。改用倒排索引的方式如下

关键字|文章倒排列表(出现文章，文章中出现的单词位置，出现次数/词频)
-|-
python|(文章A,<1,3>,2),(文章B,<3>,1),(文章C,<2>,1)
django|(文章A,<2>,1),(文章C,<5>,1)
ruby|(文章B,<1>,1)

倒排索引需要解决的问题
1. 大小写转换问题，python和PYTHON
2. 词干抽取，look和looking
3. 分词，电脑桌面还是电脑，桌面
4. 倒排文件过大，压缩编码

## 使用
通过kibana,来操作es。启动kibana，选择Dev Tools，即可在输入框起飞了~
