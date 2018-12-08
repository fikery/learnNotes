## elasticsearch基本介绍
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
2. 安装[elasticsearch-rtf](https://github.com/medcl/elasticsearch-rtf)（国内大神集成了很多插件的版本）
3. 安装[head插件](https://github.com/mobz/elasticsearch-head)
4. 安装[kibana](https://www.elastic.co/cn/downloads/kibana) 需要注意的是要安装与rtf对应的版本
