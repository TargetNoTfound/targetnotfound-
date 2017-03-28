# sqlserver 架构与基本表 
## 1. 数据库的创建与管理
### [1.1 create database （创建数据库）](#1.1)
### [1.2 alter database (修改数据库)](#1.2)
### [1.3 shrinkdatabase（收缩数据库）](#1.3)
### [1.4 drop database (删除数据库)](#1.4)
### [1.5 detach and attach database (分离与附加数据库)](#1.5)
## 2. SQL基础
### [2.1 数据类型](#2.1)


<h3 id="1.1">1.1 create database （创建数据库）

*[CREATE DATABASE (Transact-SQL)](https://msdn.microsoft.com/zh-cn/library/ms176061\(v=sql.105\).aspx)* 

```sql
CREATE DATABASE database_name 
    [ ON 
        { [ PRIMARY ] [ <filespec> [ ,...n ] 
        [ , <filegroup> [ ,...n ] ] 
    [ LOG ON { <filespec> [ ,...n ] } ] }
   ]

<filespec> ::= 
{
(
    NAME =logical_file_name,
    FILENAME = { 'os_file_name' | 'filestream_path' } 
        [ , SIZE =size [ KB | MB | GB | TB ] ] 
        [ , MAXSIZE = { max_size [ KB | MB | GB | TB ] | UNLIMITED } ] 
        [ , FILEGROWTH =growth_increment [ KB | MB | GB | TB | % ] ]
) [ ,...n ]
}

<filegroup> ::= 
{
FILEGROUP filegroup_name [ CONTAINS FILESTREAM ] [ DEFAULT ]
    <filespec> [ ,...n ]
}

```

#### 示例
以下示例创建数据库 `Sales`，该数据库具有以下文件组：

   * 包含文件 `Spri1_dat` 和 `Spri2_dat` 的主文件组。将这些文件的 `FILEGROWTH` 增量指定为 15%。

    * 名为 `SalesGroup1` 的文件组，其中包含文件 `SGrp1Fi1` 和 `SGrp1Fi2`。

   * 名为 `SalesGroup2` 的文件组，其中包含文件 `SGrp2Fi1` 和 `SGrp2Fi2`。

此示例将数据和日志文件放置于不同的磁盘上，以便提高性能。
```sql
CREATE DATABASE Sales
ON PRIMARY
( NAME = SPri1_dat,
    FILENAME = 'D:\SalesData\SPri1dat.mdf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 15% ),
( NAME = SPri2_dat,
    FILENAME = 'D:\SalesData\SPri2dt.ndf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 15% ),
FILEGROUP SalesGroup1
( NAME = SGrp1Fi1_dat,
    FILENAME = 'D:\SalesData\SG1Fi1dt.ndf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 5 ),
( NAME = SGrp1Fi2_dat,
    FILENAME = 'D:\SalesData\SG1Fi2dt.ndf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 5 ),
FILEGROUP SalesGroup2
( NAME = SGrp2Fi1_dat,
    FILENAME = 'D:\SalesData\SG2Fi1dt.ndf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 5 ),
( NAME = SGrp2Fi2_dat,
    FILENAME = 'D:\SalesData\SG2Fi2dt.ndf',
    SIZE = 10,
    MAXSIZE = 50,
    FILEGROWTH = 5 )
LOG ON
( NAME = Sales_log,
    FILENAME = 'E:\SalesLog\salelog.ldf',
    SIZE = 5MB,
    MAXSIZE = 25MB,
    FILEGROWTH = 5MB ) ;
```


<h3 id="1.2">1.2 alter database (修改数据库)


*[ALTER DATABASE 文件和文件组选项 (Transact-SQL)](https://msdn.microsoft.com/zh-cn/library/bb522469\(v=sql.105\).aspx)* 

```sql

ALTER DATABASE database_name 
{
    <add_or_modify_files>
  | <add_or_modify_filegroups>
}
[;]

<add_or_modify_files>::=
{
    ADD FILE <filespec> [ ,...n ] 
        [ TO FILEGROUP { filegroup_name } ]
  | ADD LOG FILE <filespec> [ ,...n ] 
  | REMOVE FILE logical_file_name 
  | MODIFY FILE <filespec>
}

<filespec>::= 
(
    NAME = logical_file_name  
    [ , NEWNAME = new_logical_name ] 
    [ , FILENAME = {'os_file_name' | 'filestream_path' } ] 
    [ , SIZE = size [ KB | MB | GB | TB ] ] 
    [ , MAXSIZE = { max_size [ KB | MB | GB | TB ] | UNLIMITED } ] 
    [ , FILEGROWTH = growth_increment [ KB | MB | GB | TB| % ] ] 
    [ , OFFLINE ]
) 

```
#### 示例
A.向数据库中添加由两个文件组成的文件组

以下示例在` AdventureWorks2008R2 `数据库中创建文件组` Test1FG1`，然后将两个 5 MB 的文件添加到该文件组。
```sql
ALTER DATABASE AdventureWorks2008R2
ADD FILEGROUP Test1FG1;
GO
ALTER DATABASE AdventureWorks2008R2 
ADD FILE 
(
    NAME = test1dat3,
    FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL10_50.MSSQLSERVER\MSSQL\DATA\t1dat3.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
),
(
    NAME = test1dat4,
    FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL10_50.MSSQLSERVER\MSSQL\DATA\t1dat4.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
)
TO FILEGROUP Test1FG1;
```
B.从数据库中删除文件
以下示例删除示例 A 中添加的一个文件。
```sql
ALTER DATABASE AdventureWorks2008R2
REMOVE FILE test1dat4;
```

C.修改文件
以下示例增加示例 B 中添加的一个文件的大小。
```sql
ALTER DATABASE AdventureWorks2008R2 
MODIFY FILE
    (NAME = test1dat3,
    SIZE = 20MB);
```


<h3 id="1.3">1.3 shrinkdatabase（收缩数据库)<h3>


*[DBCC SHRINKFILE (Transact-SQL)](https://msdn.microsoft.com/zh-cn/library/ms189493.aspx)*

>收缩当前数据库的指定数据或日志文件的大小，或通过将数据从指定的文件移动到相同文件组中的其他文件来清空文件，以允许从数据库中删除该文件。
>文件大小可以收缩到比创建该文件时所指定的大小更小。 这样会将最小文件大小重置为新值。


```sql
DBCC SHRINKFILE   
(  
    { file_name | file_id }   
    { [ , EMPTYFILE ]   
    | [ [ , target_size ] [ , { NOTRUNCATE | TRUNCATEONLY } ] ]  
    }  
)  
[ WITH NO_INFOMSGS ]  
```
#### 示例
A. 将数据文件收缩到指定的目标大小

下面的示例收缩的名为的数据文件大小`DataFile1`中`UserDB`到 7 MB 的用户数据库。
```sql
DBCC SHRINKFILE (DataFile1, 7);
```


<h3 id="1.4">1.4 drop database (删除数据库)

*[DROP DATABASE (Transact-SQL)](https://msdn.microsoft.com/zh-cn/library/ms178613(v=sql.105).aspx)*
#### 语法
```sql
DROP DATABASE { database_name | database_snapshot_name } [ ,...n ] 
[;]
```
#### 示例
A. 删除单个数据库

以下示例删除 `Sales` 数据库。
```sql
DROP DATABASE Sales;
```



<h3 id="1.5">1.5 detach and attach database (分离与附加数据库)

*[分离与附加数据库](https://msdn.microsoft.com/zh-cn/library/ms190794(v=sql.105).aspx)*



