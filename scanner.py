from scapy.all import ARP, Ether, srp, conf
from port_scanner import scan_ports
import socket
from database import create_table, save_device

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "Bilinmiyor"

def scan_network(ip_range):
    arp_request = ARP(pdst=ip_range)

    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = broadcast / arp_request

    result = srp(
    packet,
    timeout=5,
    verbose=False
    )[0]

    devices = []

    for sent, received in result:

     ip = received.psrc

     devices.append({
        "ip": ip,
        "mac": received.hwsrc,
        "hostname": get_hostname(ip),
        "open_ports": scan_ports(ip)
     })

    #print(devices)
    return devices


if __name__ == "__main__":
    create_table()

    ip_range = input("IP Aralığı: ")

    devices = scan_network(ip_range)

    print("\nBulunan Cihazlar")
    print("-" * 40)

    if not devices:
        print("Hiçbir cihaz bulunamadı.")
    else:
        for device in devices:
            print(f"IP  : {device['ip']}")
            print(f"MAC : {device['mac']}")
            print(f"Hostname : {device['hostname']}")
            print(f"Açık Portlar: {device['open_ports']}")
            print("-" * 40)

            save_device(
                device["ip"],
                device["mac"],
                device["hostname"],
                device["open_ports"]
            )