import os
import psutil
from colorama import Fore, Style
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_color(usage):
    if usage < 50:
        return Fore.GREEN
    elif 50 <= usage <= 75:
        return Fore.YELLOW
    else:
        return Fore.RED

def display_usage():
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()

    cpu_color = get_color(cpu_usage)
    ram_color = get_color(ram_usage)

    print(
        f"CPU Usage: {cpu_color}{cpu_usage:.2f}%{Style.RESET_ALL}  RAM Usage: {ram_color}{ram_usage:.2f}%{Style.RESET_ALL}")

def main():
    try:
        while True:
            os.system("clear" if os.name == "posix" else "cls")  # Clear the terminal screen
            display_usage()
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
