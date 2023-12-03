import ipaddress
import socket

def is_device_reachable(ip, port):
    try:
        # 尝试建立 socket 连接
        with socket.create_connection((ip, port), timeout=3):
            return True
    except (socket.timeout, socket.error):
        # print(ip + "设备" + port + "无法访问")
        return False


# 示例
def main():
    reachable = is_device_reachable("192.168.0.1", 22)
    print(reachable)


if __name__ == "__main__":
    main()
