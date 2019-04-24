var http = new XMLHttpRequest();
var cookie = {"JSESSIONID": "CDa2dgNuAvnTqbXgxyoPw"};
var params = 'zjh=201551010&mm=1035679856';
http.open("POST", chrome.extension.getURL('http://zhjw.dlut.edu.cn/loginAction.do'), true);
http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
http.overrideMimeType('application/xml');
// http.setRequestHeader('Cookie', 'JSESSIONID=CDa2dgNuAvnTqbXgxyoPw');
/*
    XMLHTTP.readyState的五种就绪状态：
        0：请求未初始化（还没有调用 open()）。
        1：请求已经建立，但是还没有发送（还没有调用 send()）。
        2：请求已发送，正在处理中（通常现在可以从响应中获取内容头）。
        3：请求在处理中；通常响应中已有部分数据可用了，但是服务器还没有完成响应的生成。
        4：响应已完成；您可以获取并使用服务器的响应了。
 */
http.onreadystatechange = function() {  //Call a function when the state changes.
    if(http.readyState === 4 && http.status === 200) {
        var parser = new DOMParser();
        var xmlDoc = parser.parseFromString(http.responseText, "application/xml");
        alert(xmlDoc);
        var text = xmlDoc.getElementsByTagName('body');
        /* 0 ? */
        alert(text.length);
    }
};
http.send(params);
