# 导入套接字模块
import socket
# 导入线程模块
import threading
import pandas as pd
import time

from sympy.physics.vector import frame

filecsv = pd.read_csv("./result-3_924.csv", sep=',')
Yaw = filecsv["Yaw"]
Pitch = filecsv["Pitch"]
Roll = filecsv["Roll"]
IMU_Yaw = filecsv["IMU_Yaw"]
IMU_Pitch = filecsv["IMU_Pitch"]
IMU_Roll = filecsv["IMU_Roll"]
package = [Yaw, Pitch, Roll, IMU_Yaw, IMU_Pitch, IMU_Roll]
frames = 0
length = Yaw.__len__()
def read_data2(package, frames):
    yaw = package[0][frames]*0.3+package[3][frames]*0.7
    pitch = package[1][frames]*0.3+package[4][frames]*0.7
    roll = package[2][frames]*0.1+package[5][frames]*0.9
    return [yaw, pitch, roll]

def read_data3(package, frames):
    b = 3
    yaw = package[0+b][frames]
    pitch = package[1+b][frames]
    roll = package[2+b][frames]
    return [yaw, pitch, roll]
# 定义个函数,使其专门重复处理客户的请求数据（也就是重复接受一个用户的消息并且重复回答，直到用户选择下线）
def send(tcp_client_1,x):
    global frames,package
    # 5 循环接收和发送数据
    while True:
        data = read_data3(package,frames)
        tcp_client_1.send(f"({data[0]},{data[1]},{-data[2]})".encode("utf-8"))
        frames = frames + 1
        time.sleep(0.05*1.2787)
        # if frames == length:
        #     frames=0




if __name__ == '__main__':

    tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2 通过客户端套接字的connect方法与服务器套接字建立连接
    # 参数介绍：前面的ip地址代表服务器的ip地址，后面的61234代表服务端的端口号 。

    tcp_client_1.connect(("192.168.3.8", 25001))

    # 4 循环等待客户端连接请求（也就是最多可以同时有128个用户连接到服务器进行通信）

    thd_send = threading.Thread(target=send, args=(tcp_client_1,288))

    # 设置守护主线程  即如果主线程结束了 那子线程中也都销毁了  防止主线程无法退出
    # thd.setDaemon(True)

    # 启动子线程对象
    thd_send.start()

    # 7 关闭服务器套接字 （其实可以不用关闭，因为服务器一直都需要运行）
    # tcp_server.close()

