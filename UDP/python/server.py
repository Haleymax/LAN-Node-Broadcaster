import socket
import threading


node_info = {
    "10.86.112.36": "mac_mini_5",
    "10.86.96.203": 'mac_mini_10',
    "10.86.96.199": 'mac_mini_7',
    "10.86.96.200": 'mac_mini_9',
    "10.86.97.157": 'loclhost',
    "10.86.120.151": 'macbook_air',
    "10.86.97.62": "ubuntu",
    "10.86.96.198": "mac-mini-6"
}

url = 'https://open.feishu.cn/open-apis/bot/v2/hook/f932c630-b938-40a9-9a18-f50f32d561c3'


class Server:
    def __init__(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 使用 UDP
        self.address = (host, port)

    def start(self):
        self.sock.bind(self.address)
        print('Server is listening on {}:{}'.format(*self.address))

    def receive(self):
        while True:
            try:
                # 接收 UDP 数据报
                msg, client_address = self.sock.recvfrom(1024)
                if msg:
                    data = msg.decode('utf-8')
                    info = data.split('-')
                    host = info[0]
                    current_memory = int(info[1])
                    total_memory = int(info[2])
                    print(f'Received info from {client_address}: {info}')

                    t = threading.Thread(target=self.check, args=(host, current_memory, total_memory))
                    t.start()
            except Exception as e:
                print(f"接收数据时出错: {e}")

    def check(self, host: str, current_memory: int, total_memory: int):
        pass

        percentage = (current_memory / total_memory) * 100
        if percentage > 80:
            print(f"当前内存占比为: {percentage}%，已超过总内存 80%")



if __name__ == "__main__":
    server = Server('0.0.0.0', 13579)
    server.start()
    server.receive()