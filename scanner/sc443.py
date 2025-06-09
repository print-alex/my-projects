import scapy.all as scapy
import ipaddress
import sys
import requests

def get_ip_range():
    ip_range = input("Enter the IP range to scan (e.g., 192.168.1.1-192.168.1.10): ")
    start_ip, end_ip = map(str.strip, ip_range.split('-'))

    # Convert start and end IPs to integers
    start_ip_int = int(ipaddress.IPv4Address(start_ip))
    end_ip_int = int(ipaddress.IPv4Address(end_ip))

    # Generate the list of IP addresses
    ip_range_list = [str(ipaddress.IPv4Address(ip)) for ip in range(start_ip_int, end_ip_int + 1)]
    return ip_range_list

def scan_vpn(ip_range, port):
    try:
        total_ips = len(ip_range)
        successful_vpn_count = 0

        # Display initial progress
        sys.stdout.write("Progress: 0.00% - Successful VPNs: 0")
        sys.stdout.flush()

        with open("results.txt", "w") as results_file:
            for index, ip in enumerate(ip_range, start=1):
                # Crafting a packet with a SYN flag (TCP)
                packet = scapy.IP(dst=ip) / scapy.TCP(dport=port, flags="S")

                # Sending the packet and waiting for a response
                response = scapy.sr1(packet, timeout=1, verbose=0)

                # Checking if a response was received
                if response and response.haslayer(scapy.TCP) and response.getlayer(scapy.TCP).flags == 0x12:
                    print(f"\r[+] {ip}:{port} is open (VPN might be present)", end="")
                    results_file.write(f"{ip}:{port}\n")
                    results_file.flush()  # Ensure the result is immediately written to the file
                    successful_vpn_count += 1
                else:
                    print(f"\r[-] {ip}:{port} is closed", end="")

                # Display progress on a single line
                progress_percentage = (index / total_ips) * 100
                sys.stdout.write(f"\rProgress: {progress_percentage:.2f}% - Successful VPNs: {successful_vpn_count}")
                sys.stdout.flush()

        print("\nVPN scan completed.")
        print(f"Total successful VPN connections: {successful_vpn_count}")

        # Check VPN connection for each successful IP in results.txt
        print("\nChecking VPN connections...")
        with open("results.txt", "r") as results_file:
            successful_ips = results_file.read().splitlines()

        for ip in successful_ips:
            ip, port = ip.split(':')
            if check_vpn_connection(ip, int(port)):
                # Additional actions if the VPN connection is successful
                pass

        # Proxy checker for successful VPN IPs
        check_and_save_proxies(successful_ips)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close Scapy socket explicitly to avoid the AttributeError
        scapy.conf.L3socket().close()

def check_and_save_proxies(vpn_ips):
    try:
        total_vpn_ips = len(vpn_ips)
        successful_proxy_count = 0

        # Display initial progress
        sys.stdout.write("Progress: 0.00% - Successful Proxies: 0")
        sys.stdout.flush()

        with open("proxy.txt", "w") as proxy_file:
            for index, vpn_ip in enumerate(vpn_ips, start=1):
                ip, port = vpn_ip.split(':')
                if check_proxy_connection(ip, int(port)):
                    proxy_file.write(f"{ip}:{port}\n")
                    proxy_file.flush()  # Ensure the result is immediately written to the file
                    successful_proxy_count += 1

                # Display progress on a single line
                progress_percentage = (index / total_vpn_ips) * 100
                sys.stdout.write(f"\rProgress: {progress_percentage:.2f}% - Successful Proxies: {successful_proxy_count}")
                sys.stdout.flush()

        print("\nProxy check completed.")
        print(f"Total successful proxy connections: {successful_proxy_count}")

    except Exception as e:
        print(f"Error: {str(e)}")

def check_proxy_connection(ip, port):
    try:
        # Use the requests library to check if the IP acts as an HTTP proxy
        proxies = {"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"}
        response = requests.get("http://www.example.com", proxies=proxies, timeout=1)
        
        if response.status_code == 200:
            print(f"\r[+] Successful proxy connection to {ip}:{port}")
            return True
        else:
            print(f"\r[-] Unable to connect to {ip}:{port} as proxy")
            return False

    except Exception as e:
        print(f"\r[-] Unable to connect to {ip}:{port} as proxy (Error: {str(e)})")
        return False

# Example usage
ip_range = get_ip_range()
target_port = 443  # Replace with the target port
scan_vpn(ip_range, target_port)
