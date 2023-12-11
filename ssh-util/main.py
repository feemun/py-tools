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


def check_devices_availability(ip_list):
    for ip in ip_list:
        if is_ssh_available(ip):
            device_info = get_device_info(ip, 22, "catfish", "catfish")
            print(device_info)


def is_ssh_available(ip, port=22, username="catfish", password="catfish"):
    try:
        # 创建 SSH 客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 尝试连接
        client.connect(ip, port=port, username=username, password=password, timeout=1)
        # 关闭连接
        client.close()
        print("连接成功" + ip)
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.timeout):
        print("连接失败" + ip)
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
        client.connect(ip, port=port, username=username, password=password, timeout=1)
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


# 获取网段下所有ip
# 遍历所有设备
# 输入ip，端口，用户名，密码船舰ssh连接
# 如果ssh连接成功，则返回主机信息

if __name__ == '__main__':
    subnet = get_all_ips_in_subnet("192.168.31.1/24")
    check_devices_availability(subnet)
