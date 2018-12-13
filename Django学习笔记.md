WSGI server的作用：
* 监听HTTP服务的端口(80端口)
* 接收浏览器端HTTP的请求并解析封装成environ环境数据
* 调用APP应用程序，传入environ和start_response方法
* 封装APP返回的数据成HTTP响应报文，传递给浏览器
