#!/usr/bin/env python
#coding=utf8
 
from socket import *
 
host = '10.105.249.4'
port = 12346
bufsiz = 1024
 
#开启套接字
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#绑定服务端口
tcpSerSock.bind((host, port))
#开始监听
tcpSerSock.listen(5)
 
while True:
    #等待客户端连接
    print 'waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from:', addr
    tcpCliSock.send('%s' %("rilegoulable"))
 
    while True:
        #接收客户端信息
        data = tcpCliSock.recv(bufsiz)
        if not data:
            break
        #给客户端发送信息
        tcpCliSock.send('[%s] %s' %("You send:", data))
        print data
 
    tcpCliSock.close()
 
tcpSerSock.close()
