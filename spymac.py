#!/usr/bin/env python3

import subprocess
import re
import time
import sys
import os
import random
import argparse
from datetime import datetime
from termcolor import colored

def display_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    banner = """
███╗   ███╗ █████╗  ██████╗     ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
████╗ ████║██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
██╔████╔██║███████║██║         ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
██║╚██╔╝██║██╔══██║██║         ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║  ██║╚██████╗    ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    print(colored(banner, 'green'))
    print(colored("                      Developed by AnonSpyDir\n", 'red', attrs=['bold']))
    animate(colored(">> Activating SPY Modules...\n", 'yellow'))
    time.sleep(0.5)

def animate(text, delay=0.03):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def generate_random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))

def is_valid_mac(mac):
    return re.match(r"^\w\w:\w\w:\w\w:\w\w:\w\w:\w\w$", mac)

def get_current_mac(interface):
    try:
        result = subprocess.check_output(["ifconfig", interface], stderr=subprocess.DEVNULL).decode()
        match = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result)
        return match.group(0) if match else None
    except:
        return None

def list_interfaces():
    try:
        output = subprocess.check_output("ifconfig", shell=True).decode()
        interfaces = re.findall(r"^(\w+):", output, re.MULTILINE)
        return [iface for iface in interfaces if iface != "lo"]
    except:
        return []

def log_mac_change(interface, old_mac, new_mac, success):
    with open("spylog.txt", "a") as log:
        status = "SUCCESS" if success else "FAILED"
        log.write(f"[{datetime.now()}] {interface} | {old_mac} -> {new_mac} | {status}\n")

def change_mac(interface, new_mac):
    try:
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
    except:
        animate(colored("[!] MAC change command failed", 'red'))

def run_mac_change(interface, new_mac):
    old_mac = get_current_mac(interface)
    if old_mac:
        animate(colored(f"[✔] Current MAC: {old_mac}", 'cyan'))
    else:
        animate(colored("[!] Could not read current MAC.", 'red'))
        return

    animate(colored(f"[*] Changing MAC on {interface} to {new_mac}", 'yellow'))
    change_mac(interface, new_mac)
    time.sleep(1)

    updated_mac = get_current_mac(interface)
    if updated_mac == new_mac:
        animate(colored(f"[✔] MAC changed to: {updated_mac}", 'green'))
        log_mac_change(interface, old_mac, updated_mac, True)
    else:
        animate(colored("[!] MAC change failed!", 'red'))
        log_mac_change(interface, old_mac, new_mac, False)

def interactive_menu():
    display_banner()
    interfaces = list_interfaces()
    if not interfaces:
        animate(colored("[!] No interfaces found!", 'red'))
        return

    print(colored("Available Interfaces:", 'cyan'))
    for idx, iface in enumerate(interfaces):
        print(colored(f"{idx + 1}. {iface}", 'yellow'))

    try:
        choice = int(input(colored("\n[?] Select interface number: ", 'blue')))
        interface = interfaces[choice - 1]
    except:
        animate(colored("[!] Invalid choice.", 'red'))
        return

    print(colored("\nChoose an option:", 'cyan'))
    print(colored("1. Enter MAC manually", 'yellow'))
    print(colored("2. Generate random MAC", 'yellow'))
    print(colored("3. Exit", 'yellow'))

    opt = input(colored(">> ", 'magenta')).strip()

    if opt == '1':
        new_mac = input(colored("\n[?] Enter new MAC address: ", 'blue')).strip()
        if not is_valid_mac(new_mac):
            animate(colored("[!] Invalid MAC format.", 'red'))
            return
    elif opt == '2':
        new_mac = generate_random_mac()
        animate(colored(f"[+] Random MAC generated: {new_mac}", 'magenta'))
    elif opt == '3':
        animate(colored("[-] Exiting. Stay anonymous, agent.", 'yellow'))
        sys.exit()
    else:
        animate(colored("[!] Invalid option.", 'red'))
        return

    run_mac_change(interface, new_mac)

def cli_mode():
    parser = argparse.ArgumentParser(description="SPY MAC Changer by AnonSpyDir")
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to spoof")
    parser.add_argument("-m", "--mac", dest="new_mac", help="MAC address to assign")
    parser.add_argument("-r", "--random", action="store_true", help="Use a random MAC address")

    args = parser.parse_args()

    if not args.interface:
        parser.error("[-] Interface is required.")
    if not args.new_mac and not args.random:
        parser.error("[-] Provide --mac or use --random")

    new_mac = generate_random_mac() if args.random else args.new_mac
    if not is_valid_mac(new_mac):
        print(colored("[!] Invalid MAC format", 'red'))
        sys.exit()

    run_mac_change(args.interface, new_mac)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
    else:
        while True:
            interactive_menu()
            again = input(colored("\n[?] Spoof again? (y/n): ", 'blue')).strip().lower()
            if again != 'y':
                animate(colored("[-] Logging out. Stay Anonymous.", 'yellow'))
                break
