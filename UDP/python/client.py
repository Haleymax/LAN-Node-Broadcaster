import socket
import time
import platform
import shutil

class DiskUsageSender:
    def __init__(self, broadcast_address):
        self.broadcast_address = broadcast_address

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"获取IP地址时发生错误: {e}")
            return "Unknown"

    def get_disk_usage(self):
        system = platform.system()
        if system == "Linux" or system == "Darwin":
            try:
                usage = shutil.disk_usage('/')
                return usage.used, usage.total
            except Exception as e:
                print(f"获取磁盘使用信息时出错: {e}")
                return 0, 0
        elif system == "Windows":  # Windows 系统
            try:
                usage = shutil.disk_usage('C:\\')
                return usage.used, usage.total
            except Exception as e:
                print(f"获取磁盘使用信息时出错: {e}")
                return 0, 0
        else:
            print(f"不支持的操作系统: {system}")
            return 0, 0

    def send_disk_usage(self):
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # 启用广播模式
                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

                used_space, total_space = self.get_disk_usage()
                local_ip = self.get_local_ip()
                message = f'{local_ip}-{used_space}-{total_space}'
                print(message)

                client_socket.sendto(message.encode('utf-8'), self.broadcast_address)
                client_socket.close()
            except socket.error as e:
                print(f"发送数据时出错: {e}，")
            time.sleep(60 * 60)

    def start_sending(self):
        while True:
            self.send_disk_usage()
            print('Sent disk usage info. Next check in 60 minutes...')
            time.sleep(60 * 60)

if __name__ == "__main__":
    broadcast_address = ('255.255.255.255', 13579)
    sender = DiskUsageSender(broadcast_address)
    sender.start_sending()