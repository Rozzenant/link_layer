import psutil


def get_wireless_ip():
    interfaces = psutil.net_if_addrs()
    wireless_interfaces = [interface for interface in interfaces.keys() if 'Беспроводная сеть' in interface]
    if wireless_interfaces:
        wireless_interface = wireless_interfaces[0]
        addresses = interfaces[wireless_interface]
        ipv4_addresses = [addr for addr in addresses if addr.family == 2]
        if ipv4_addresses:
            return ipv4_addresses[0].address
        else:
            print("Беспроводный интерфейс не найден или не имеет IP-адресов.\nАдрес будет заменен на 127.0.0.1")
            return "127.0.0.1"
    print("Беспроводный интерфейс не найден или не имеет IP-адресов.\nАдрес будет заменен на 127.0.0.1")
    return "127.0.0.1"