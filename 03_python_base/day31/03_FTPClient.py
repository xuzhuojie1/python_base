import os
import socket
import struct
import json

KEY_IP_PORT = ("127.0.0.1", 8000)
KEY_UTF8 = "utf-8"
KEY_BACKLOG = 5
KEY_BUFFER_SIZE = 1024

class FTPClient:
    def __init__(self, address, connet=True):
        self.server_address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if connet:
            try:
                self.client_connet()
            except Exception as e:
                print("链接服务出现异常，ftp_client 关闭")
                self.client_close()
                raise

    def client_connet(self):
        self.socket.connect(self.server_address)

    def client_close(self):
        self.socket.close()

    def run(self):
        while True:
            try:
                inp = input(">>>").strip()
                if not inp:break
                if inp == "quit": break
                args_list = inp.split()
                cmd = args_list[0]
                if hasattr(self, cmd):
                    func = getattr(self, cmd)
                    func(args_list)
                else:
                    print("不支持操作：{}".format(inp))
            except Exception as e:
                print("客户端异常退出")
                raise
                break

    def put(self, args):
        # 校验输入参数是否正确
        if len(args) < 2:
            print("参数长度不争取：{}".format(str(args)))
            return
        filename = args[1]
        if not os.path.isfile(filename):
            print("文件 {} 不存在".format(filename))
            return
        filesize = os.path.getsize(filename)

        # 拼接报文头
        head_dic = {
            "cmd": args[0],
            "filename": os.path.basename(filename),
            "filesize": filesize}
        head_json_str = json.dumps(head_dic)
        print("发送的报文头： {}".format(head_json_str))
        head_bytes = head_json_str.encode(KEY_UTF8)
        head_len_bytes = struct.pack("i", len(head_bytes))

        #发送数据
        self.socket.send(head_len_bytes)
        self.socket.send(head_bytes)
        send_size = 0
        with open(filename, 'rb') as f:
            for line in f:
                self.socket.send(line)
                send_size += len(line)
                print("已经发送大小：{}".format(send_size))
            else:
                print("文件发送成功")


if __name__ == '__main__':
    print("启动客户端。。。")
    client = FTPClient(KEY_IP_PORT)
    client.run()


"""
    测试的时候出现报错：ConnectionAbortedError: [WinError 10053] 你的主机中的软件中止了一个已建立的连接。
    最后发现是服务端接收的时候计算接收长度没有按照实际的接收，而是使用 buffer_size 进行添加，
    将服务端中代码 recv_size += size  改为 recv_size += len(recv_msg) 解决
    
"""