import socket
import termcolor
import re

class PortScanner :
    def __init__(self) :
        self.open_count = 0

    def validate_ipv4_address(self, ip) :
        # Define the regex pattern for a valid IPv4 address
        ipv4_pattern = re.compile(
            r'^('
            r'(25[0-5]|'          # matches 250-255
            r'2[0-4][0-9]|'       # matches 200-249
            r'1[0-9][0-9]|'       # matches 100-199
            r'[1-9][0-9]|'        # matches 10-99
            r'[0-9])'             # matches 0-9
            r'\.){3}'             # for 3 occurrences followed by "dot"
            r'(25[0-5]|'
            r'2[0-4][0-9]|'
            r'1[0-9][0-9]|'
            r'[1-9][0-9]|'
            r'[0-9])$'
        )
        
        # Match the input IP against the regex pattern
        if ipv4_pattern.match(ip) :
            return True
        else :
            return False

    def scan(self, target, ports) :
        if not self.validate_ipv4_address(target) :
            print(termcolor.colored(("Invalid IP address: " + str(target)), 'red'))
            return
        
        print(termcolor.colored(("\n" + "Scanning Target: " + str(target)), 'yellow'))
        self.open_count = 0  # Reset open_count for each target scan

        for port in ports :
            self.port_scan(target, port)

        print("\n" + "Number of Ports Opened: " + str(self.open_count))
        close_count = len(ports) - self.open_count
        print("Number of Ports Closed: " + str(close_count) + "\n")

    def port_scan(self, ipaddress, port) :
        try :
            sockObj = socket.socket()
            sockObj.settimeout(1)  # Set a timeout for the connection attempt
            sockObj.connect((ipaddress, port))  # Passing arguments
            print(termcolor.colored(("[+] Port Opened " + str(port)), 'green'))
            self.open_count += 1
            sockObj.close()
        except :
            pass

    def parse_comma_separated_ports(self, port_input) :
        ports = set()
        for part in port_input.split(',') :
            ports.add(int(part.strip()))  # Use strip to clean each port
        return sorted(ports)

    def parse_port_range(self, port_range) :
        start, end = port_range.split('-')
        return list(range(int(start.strip()), int(end.strip()) + 1))

if __name__ == "__main__" :
    scanner = PortScanner()
    targets = input("[*] Enter the Target's IP addresses (split them by '-') : ")

    print(termcolor.colored("[*] Press 1 : To scan a set of ports", 'yellow'))
    print(termcolor.colored("[*] Press 2 : To scan range of ports", 'yellow'))
    option = input("[*] Enter Option : ")

    if option == '1' :
        port_input = input("[*] Enter Ports to be scanned like [22,80,443]: ")
        ports = scanner.parse_comma_separated_ports(port_input)
    elif option == '2' :
        port_range = input("[*] Enter Ports to be scanned like [1-100]: ")
        ports = scanner.parse_port_range(port_range)
    else :
        print("Invalid Option")
        exit()

    if '-' in targets :
        print(termcolor.colored("[*] Scanning Multiple Targets: ", 'blue'))
        for ip_addr in targets.split('-'):  # For loop for scanning multiple targets using split function
            scanner.scan(ip_addr.strip(), ports)
    else :
        scanner.scan(targets.strip(), ports)
