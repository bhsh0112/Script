import scapy.all as scapy
import netifaces as ni

def get_my_ip():
    # 获取本机的 IP 地址
    try:
        # 获取默认网关接口
        gateway_interface = ni.gateways()['default'][ni.AF_INET][1]
        # 获取该接口的 IP 地址
        my_ip = ni.ifaddresses(gateway_interface)[ni.AF_INET][0]['addr']
        return my_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

def get_network_range(my_ip):
    # 从 IP 地址中提取网络范围（假设子网掩码为 255.255.255.0）
    ip_parts = my_ip.split('.')
    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1/24"
    return network_range

def scan_network(network_range):
    # 使用 Scapy 发送 ARP 请求并解析响应
    try:
        # 发送 ARP 请求
        arp_request = scapy.ARP(pdst=network_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        # 解析响应并提取设备信息
        devices = []
        for element in answered_list:
            device_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device_info)
        return devices
    except Exception as e:
        print(f"Error scanning network: {e}")
        return []

def print_devices(devices):
    # 打印发现的设备
    print("Devices in the network:")
    print(f"{'IP Address':<20}{'MAC Address':<20}")
    for device in devices:
        print(f"{device['ip']:<20}{device['mac']:<20}")

if __name__ == "__main__":
    # 获取本机 IP 地址
    my_ip = get_my_ip()
    if my_ip:
        print(f"My IP address: {my_ip}")
        # 获取网络范围
        network_range = get_network_range(my_ip)
        print(f"Scanning network range: {network_range}")
        # 扫描网络
        devices = scan_network(network_range)
        # 打印设备信息
        print_devices(devices)
    else:
        print("Failed to get local IP address.")