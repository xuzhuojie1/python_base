"""
select 模拟一个 socket server，注意 socket 必须在非阻塞情况下才能实现 IO 多路复用。
        接下来通过了解 select 是如何通过单进程实现同时处理多个非阻塞的 socket 链接的。
"""
#========== server 端 ==========
import select
import socket
import queue

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(1000)
server.setblocking(False)  # 设置成非阻塞，accept 和 recv 都是非阻塞的
# 这里如果直接 server.accept() ，如果没有连接会报错，所以有数据才调他们
# BlockIOError：[WinError 10035] 无法立即完成一个非阻塞性套接字操作。

msg_dic = {}
inputs = [server]  # 交给内核，select 检测列表
# 这里如果直接 server.accept() ，如果没有连接会报错，所以有数据才调他们
# BlockIOError：[WinError 10035] 无法立即完成一个非阻塞性套接字操作。
outputs = []  # 你往里面放什么，下一次就出来了

print("启动服务端监听。。。")
while True:
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)  # 定义检测
    # (inputs 【检测列表】, outputs, inputs 【异常（断开）】)
    print("readable = {}, writeable = {}, exceptional = {}".format(
        readable, writeable, exceptional ))

    for r in readable:
        if r is server:  # 有数据，代表一个新连接
            conn, addr = server.accept()
            print("来了个新链接：{}".format(addr))
            inputs.append(conn)  # 把连接加到检测列表里，如果这个连接活动了，就说明数据来了
            msg_dic[conn] = queue.Queue()  # 初始化一个队列，后面存要返回给这个客户端的数据
        else:
            try:
                data = r.recv(1024)  # 注意这里是r，而不是conn，多个连接的情况
                print("收到数据：{}".format(data))
                msg_dic[r].put(data)  # 往里面放数据
                outputs.append(r)  # 放入返回的连接队列里
            except ConnectionResetError as e:
                print("客户端断开了：{}".format(r))
                if r in outputs:
                    outputs.remove(r) #清理已断开的连接
                inputs.remove(r) #清理已断开的连接
                del msg_dic[r] #清理已断开的连接对应的消息队列

    for w in writeable:  # 要返回给客户端的连接列表
        data_to_client = msg_dic[w].get()  # 在字典里取数据
        w.send(data_to_client)  # 返回给客户端
        outputs.remove(w)  # 删除这个数据，确保下次循环的时候不返回这个已经处理完的连接了。

    for e in exceptional:  # 如果连接断开，删除连接相关数据
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)
        del msg_dic[e]
