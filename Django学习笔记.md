WSGI server的作用：
* 监听HTTP服务的端口(80端口)
* 接收浏览器端HTTP的请求并解析封装成environ环境数据(包含HTTP请求信息的dict对象)
* 调用APP应用程序，传入environ和start_response方法
* 封装APP返回的数据成HTTP响应报文，传递给浏览器


web服务器：
* 本质上是一个tcp服务器，监听特定端口
* 支持HTTP协议，能够将HTTP请求报文解析，能够把响应数据封装成HTTP响应报文，再发给浏览器
* 实现了WSGI协议，该协议约定了和应用程序之间的接口

