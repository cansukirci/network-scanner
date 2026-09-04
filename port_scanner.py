import socket

def scan_ports(ip):
    ports = [22, 80, 443, 8000]
    open_ports = []

    for port in ports:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        result = sock.connect_ex((ip, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    return open_ports


if __name__ == "__main__":
    target_ip = input("Taranacak IP adresi: ")

    open_ports = scan_ports(target_ip)
    
    print("Açık portlar:", open_ports)