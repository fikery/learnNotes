PostgreSql是一个功能强大的开源对象关系数据库管理系统。
**特点**

1. 跨平台
2. 存储类型丰富，文本，图像，音频，视频
3. 支持SQL的诸多功能，复杂查询，外键，事务等等
4. 表可以从“父”表继承特征
5. 可安装拓展增加功能

由于psql自带的pgAdmin组件可以提供可视化数据库操作，以下仅针对于psql命令行进行记录。

**创建/删除数据库**

```
# 建库
CREATE DATABASE database_name;
# 删库
DROP DATABASE database_name;
 
# 列出数据库
\l
 
# 退出psql
\q
 ```
 
 **创建/删除表**
 
 ```
 # 创建表
 CREATE TABLE table_name(
  id int NOT NULL,
  name varchar(20),
  date DATE
 );
 
 # 删除表
 `DROP TABLEE table_name`
 ``` 
 
 **增删改查**
 
 ```
# 插入 
INSERT INTO TABLE_NAME (column1, column2, column3,...columnN)  
VALUES (value1, value2, value3,...valueN);

# 查询
SELECT "column1", "column2".."column" FROM "table_name";

# 更新
UPDATE table_name  
SET column1 = value1, column2 = value2...., columnN = valueN  
WHERE [condition];

# 删除
DELETE FROM table_name  
WHERE [condition];
 ```
**排序分组**

```
# order by
SELECT column-list  
FROM table_name  
[WHERE condition]  
[ORDER BY column1, column2, .. columnN] [ASC | DESC];

# group by
SELECT column-list  
FROM table_name  
WHERE [conditions ]  
GROUP BY column1, column2....columnN  
ORDER BY column1, column2....columnN

# having和group by组合
SELECT column1, column2  
FROM table1, table2  
WHERE [ conditions ]  
GROUP BY column1, column2  
HAVING [ conditions ]  
ORDER BY column1, column2
```

**连接**

```
# 内连接
SELECT table1.columns, table2.columns  
FROM table1  
INNER JOIN table2  
ON table1.common_filed = table2.common_field;

# 左外连接
SELECT table1.columns, table2.columns  
FROM table1  
LEFT OUTER JOIN table2  
ON table1.common_filed = table2.common_field;

# 右外连接
SELECT table1.columns, table2.columns  
FROM table1  
RIGHT OUTER JOIN table2  
ON table1.common_filed = table2.common_field;

# 全外连接
SELECT table1.columns, table2.columns  
FROM table1  
FULL OUTER JOIN table2  
ON table1.common_filed = table2.common_field;

# 笛卡尔积
SELECT coloums   
FROM table1   
CROSS JOIN table2
```
**索引**

```
# 单列索引
CREATE INDEX index_name  
ON table_name (column_name);

# 多列索引
CREATE INDEX index_name  
ON table_name (column_name1, column_name2);
```
