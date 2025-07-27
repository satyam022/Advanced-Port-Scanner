import socket
import time
import threading


print("="*50)
print("  ██████╗ ██╗   ██╗███████╗███████╗███████╗")
print("  ██╔══██╗██║   ██║██╔════╝██╔════╝██╔════╝")
print("  ██████╔╝██║   ██║█████╗  █████╗  ███████╗")
print("  ██╔═══╝ ██║   ██║██╔══╝  ██╔══╝  ╚════██║")
print("  ██║     ╚██████╔╝██║     ███████╗███████║")
print("  ╚═╝      ╚═════╝ ╚═╝     ╚══════╝╚══════╝")
print("="*50)
print("      Tool Name   : Advanced Port Scanner")
print("      Coder       : Ghost Bhoot 🧠")
print("      Status      : Initializing...\n")
print("="*50)


# 🔹 Service name nikalne ka function
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

# 🔹 Banner grabbing function
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner if banner else "No banner"
    except:
        return "No banner or connection refused"

# 🔹 Single port scan function (threading ke liye)
def scan_port(ip, port, results_lock, results):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            service = get_service_name(port)
            banner = grab_banner(ip, port)
            msg = f"[+] {ip} : Port {port} OPEN --> Service: {service} | Banner: {banner}"
            print(msg)

            # Lock lagakar thread-safe result add karna
            with results_lock:
                results.append(msg)
        s.close()
    except:
        pass

# 🔹 Main scanner function
def start_scan():
    # 🔸 Input lena
    targets_input = input("Enter IPs/domains (comma separated): ")
    targets = [t.strip() for t in targets_input.split(',')]

    port_input = input("Enter port number OR start-end range (e.g. 80 or 20-100): ")

    # 🔸 Ports parsing
    if '-' in port_input:
        try:
            start_port, end_port = map(int, port_input.split('-'))
            port_list = range(start_port, end_port + 1)
        except:
            print("❌ Invalid range format.")
            return
    else:
        try:
            port = int(port_input)
            port_list = [port]
        except:
            print("❌ Invalid port input.")
            return

    results = []
    results_lock = threading.Lock()
    start_time = time.time()

    threads = []

    for target in targets:
        try:
            ip = socket.gethostbyname(target)
            print(f"\n🔎 Scanning {target} ({ip})...\n")
            for port in port_list:
                t = threading.Thread(target=scan_port, args=(ip, port, results_lock, results))
                threads.append(t)
                t.start()
        except:
            print(f"❌ Could not resolve: {target}")
            continue

    # 🔸 Sare threads complete hone ka wait
    for t in threads:
        t.join()

    duration = round(time.time() - start_time, 2)
    print(f"\n✅ Scan completed in {duration} seconds.")

    # 🔸 Output file save
    with open("scan_output.txt", "w") as f:
        for line in results:
            f.write(line + "\n")

    print("📁 Output saved to 'scan_output.txt'")

# 🔹 Run scanner
start_scan()
