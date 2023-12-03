import ipaddress
import socket
import paramiko


# 遍历网段下的所有设备
def get_all_ips_in_subnet(subnet):
    try:
        ip_network = ipaddress.IPv4Network(subnet, strict=False)
        all_ips = [str(ip) for ip in ip_network.hosts()]
        return all_ips
    except ipaddress.AddressValueError as e:
        return f"无效的子网掩码: {e}"


def is_device_reachable(ip, port=22):
    try:
        # 尝试建立 socket 连接
        with socket.create_connection((ip, port), timeout=3):
            return True
    except (socket.timeout, socket.error):
        print(ip + "设备无法访问")
        return False


def check_devices_availability(ip_list):
    available_devices = []

    for ip in ip_list:
        if is_device_reachable(ip):
            available_devices.append(ip)

    return available_devices


def is_ssh_available(ip, port=22, username="catfish", password="catfish"):
    try:
        # 创建 SSH 客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 尝试连接
        client.connect(ip, port=port, username=username, password=password, timeout=1)

        # 关闭连接
        client.close()
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.timeout):
        return False


def get_device_info(ip, port=22, username="catfish", password="catfish"):
    device_info = {
        "IP": ip,
        "Port": port,
        "Username": username,
        "Password": password,
        "Hostname": "",
        "OS": "",
    }

    try:
        # 创建 SSH 客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 尝试连接
        client.connect(ip, port, username, password, timeout=3)

        # 获取主机名
        stdin, stdout, stderr = client.exec_command("hostname")
        device_info["Hostname"] = stdout.read().decode().strip()

        # 获取操作系统信息
        stdin, stdout, stderr = client.exec_command("uname -a")
        device_info["OS"] = stdout.read().decode().strip()

        # 关闭连接
        client.close()
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.timeout) as e:
        print(f"无法连接到 {ip}: {e}")

    return device_info


def check_ssh_availability(ip_list, port, username, password):
    ssh_available_devices = []

    for ip in ip_list:
        if is_ssh_available(ip, port, username, password):
            ssh_available_devices.append(ip)

    return ssh_available_devices


# 对所有设备发送ping
# 如果3秒没回复，则判断为设备不存在或设备禁止ping
# 如果设备回复了，则判断ssh端口是否提供服务
# 如果设备ssh端口提供服务，则使用用户名和密码登录

if __name__ == '__main__':
    # subnet = get_all_ips_in_subnet("192.168.0.100")
    # available_devices = check_devices_availability(subnet)
    # ssh_availability = check_ssh_availability(available_devices, 22, "catfish", "catfish")
    info = get_device_info("192.168.0.100", 22, "catfish", "catfish")
    print(info)
