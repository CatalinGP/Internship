import platform
import socket
import re
import paramiko

def get_local_ip():
    if platform.system() == 'Linux' or platform.system() == 'Windows':
        import socket
        return socket.gethostbyname(socket.gethostname())
    else:
        return None

def is_valid_ip(ip):
    ip_pattern = r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
    ip_pattern += r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
    ip_pattern += r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
    ip_pattern += r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None

def is_valid_port(port):
    try:
        port_num = int(port)
        return 0 < port_num <= 65535
    except ValueError:
        return False

def local_ip_decorator(func):
    def wrapper(*args, **kwargs):
        local_ip = get_local_ip()
        if local_ip:
            print(f"Local IP address: {local_ip}")
            return func(local_ip, *args, **kwargs)
        else:
            print("Unable to determine local IP address")
    return wrapper

@local_ip_decorator
def get_vm_ip(local_ip, host_ip, host_port, ssh_username, ssh_password, target_terminal):
    try:
        if not is_valid_ip(host_ip):
            print("Invalid IP address format. Please enter a valid IP address.")
            return None

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname=host_ip,
                        username=ssh_username,
                        password=ssh_password,
                        port=host_port)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print(f"Unable to connect: {str(e)}")
            return None

        stdin, stdout, stderr = ssh.exec_command("last -i")

        output = stdout.read().decode()
        ip_address_match = re.search(rf'{target_terminal}\s+\S+\s+([\d.]+)', output)

        if ip_address_match:
            ip_address = ip_address_match.group(1)
            print(f"IP Address of the target machine is {ip_address}")

            if local_ip == ip_address:
                print("Host IP and target machine IP match")
            else:
                print("Host IP and target machine IP do not match")

            ssh.close()
            return ip_address
        else:
            print("Unable to retrieve IP address from 'last -i' command.")
            ssh.close()
            return None

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check SSH username or password")
        return None

    except paramiko.SSHException as e:
        print(f"SSH Error: {str(e)}")
        return None

    except socket.gaierror as e:
        print(f"Socket error: {str(e)}")
        return None


if __name__ == "__main__":
    while True:
        host_ip = input("Enter the IP address of the target machine: ")
        if is_valid_ip(host_ip):
            break
        else:
            print("Invalid IP format.")

    while True:
        host_port = input("Enter the port of the target machine: ")
        if is_valid_port(host_port):
            break
        else:
            print("Invalid port format")

    ssh_username = input("Enter SSH username: ")
    ssh_password = input("Enter SSH password: ")
    target_terminal = input("Enter the target terminal (e.g., pts/0): ")
    get_vm_ip(host_ip, host_port, ssh_username, ssh_password, target_terminal)