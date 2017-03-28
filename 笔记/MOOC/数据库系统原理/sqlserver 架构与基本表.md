# sqlserver 架构与基本表 
## 1. 数据库的创建与管理
### [1.1 create database （创建数据库）](#1.1)
### [1.2 alter database (修改数据库)](#1.2)


<h3 id="1.1">1.1 create database （创建数据库）

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

database_name

    新数据库的名称。数据库名称在 SQL Server 的实例中必须唯一，并且必须符合标识符规则。

    除非没有为日志文件指定逻辑名称，否则 database_name 最多可以包含 128 个字符。如果未指定逻辑日志文件名称，则 SQL Server 将通过向 database_name 追加后缀来为日志生成 logical_file_name 和 os_file_name。这会将 database_name 限制为 123 个字符，从而使生成的逻辑文件名称不超过 128 个字符。

    如果未指定数据文件的名称，则 SQL Server 使用 database_name 作为 logical_file_name 和 os_file_name。默认路径从注册表中获得。可以使用 Management Studio 中的“服务器属性”（“数据库设置”页）更改默认路径。更改默认路径要求重新启动 SQL Server。
ON

    指定显式定义用来存储数据库数据部分的磁盘文件（数据文件）。当后面是以逗号分隔的、用以定义主文件组的数据文件的 <filespec> 项列表时，需要使用 ON。主文件组的文件列表可后跟以逗号分隔的、用以定义用户文件组及其文件的 <filegroup> 项列表（可选）。
PRIMARY

    指定关联的 <filespec> 列表定义主文件。在主文件组的 <filespec> 项中指定的第一个文件将成为主文件。一个数据库只能有一个主文件。有关详细信息，请参阅文件和文件组体系结构。

    如果没有指定 PRIMARY，那么 CREATE DATABASE 语句中列出的第一个文件将成为主文件。
LOG ON

    指定显式定义用来存储数据库日志的磁盘文件（日志文件）。LOG ON 后跟以逗号分隔的用以定义日志文件的 <filespec> 项列表。如果没有指定 LOG ON，将自动创建一个日志文件，其大小为该数据库的所有数据文件大小总和的 25% 或 512 KB，取两者之中的较大者。此文件放置于默认的日志文件位置。有关此位置的信息，请参阅如何查看或更改数据文件和日志文件的默认位置 (SQL Server Management Studio)。

    不能对数据库快照指定 LOG ON。

<h3 id="1.2">1.2 create database （创建数据库）