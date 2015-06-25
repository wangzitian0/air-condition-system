#!/usr/bin/env python
#coding=utf8
 
 
while True:
    #接收客户端信息
    data = raw_input("Enter your input: "); 
    if not data:
        break
    flag = data[0:2]
    room = data[2:1]
    if cmp(flag,'@#'):
        连接
    else if cmp(flag,'##'):
        temp=data[3:2]
        speed=data[5:1]
        更新temp_now
    else if cmp(flag,'-+'):
        temp=date[3:2]
        speed=data[5:1]
        更新temp_set
    else if cmp(flag,'LE'):
        断开
    #给客户端发送信息
    print data
