import threading
import time
import subprocess
import os
import psutil
from colorama import Fore, Style

FILE_PATH = 'saved_data.txt'
SYSTEM_METRICS_FILE = 'system_metrics.txt'
cmd_process = None  
system_monitoring_active = False  

def monitor_file():
    global cmd_process, system_monitoring_active
    while True:
        try:
            with open(FILE_PATH, 'r') as file:
                lines = file.readlines()  # Read all lines into a list

            # Check for 'open cmd'
            if any('open cmd' in line.strip() for line in lines):
                if cmd_process is None:
                    open_command_prompt()

            # Check for 'close cmd'
            if any('close cmd' in line.strip() for line in lines):
                if cmd_process is not None:
                    close_command_prompt()

            # Check for 'monitor system'
            if any('monitor system' in line.strip() for line in lines):
                if not system_monitoring_active:
                    print(f"{Fore.CYAN}Starting system monitoring.{Style.RESET_ALL}")
                    system_monitoring_active = True
                    start_system_monitoring()

            # Check for 'stop monitoring'
            if any('stop monitoring' in line.strip() for line in lines):
                if system_monitoring_active:
                    print(f"{Fore.YELLOW}Stopping system monitoring.{Style.RESET_ALL}")
                    system_monitoring_active = False

        except Exception as e:
            print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")

        time.sleep(1)  # Check the file every second

def open_command_prompt():
    global cmd_process
    try:
        if os.name == 'nt':  # For Windows
            if cmd_process is None:  # Ensure only one instance is opened
                cmd_process = subprocess.Popen('cmd.exe', creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # For macOS/Linux
            if cmd_process is None:  # Ensure only one instance is opened
                cmd_process = subprocess.Popen(['open', '-a', 'Terminal'])
    except Exception as e:
        print(f"{Fore.RED}Error opening command prompt: {e}{Style.RESET_ALL}")

def close_command_prompt():
    global cmd_process
    try:
        if cmd_process:
            cmd_process.terminate()  # Attempt to terminate the command prompt process
            cmd_process = None  # Reset the process reference
        else:
            print(f"{Fore.YELLOW}No command prompt process found to close.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error closing command prompt: {e}{Style.RESET_ALL}")

def monitor_system():
    while system_monitoring_active:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
            memory_info = psutil.virtual_memory()  # Get memory usage info
            memory_usage = memory_info.percent  # Get memory usage percentage

            with open(SYSTEM_METRICS_FILE, 'a') as file:
                file.write(f"{time.time()},{cpu_usage},{memory_usage}\n")
                
        except Exception as e:
            print(f"{Fore.RED}Error monitoring system: {e}{Style.RESET_ALL}")

        time.sleep(10)  # Monitor system every 10 seconds

def start_system_monitoring():
    system_monitor_thread = threading.Thread(target=monitor_system, daemon=True)
    system_monitor_thread.start()

def thrads():
    # Note: The threads created here may not function as intended since they overlap with the main script functionality
    ALL_IN_ONE = open_command_prompt, close_command_prompt, start_system_monitoring
    ALL_IN_ONE.start()
    ALL_IN_ONE.join()

if __name__ == "__main__":
    # Start the file monitoring in a separate thread
    file_monitor_thread = threading.Thread(target=monitor_file, daemon=True)
    file_monitor_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)  # Main thread sleeps to keep the program running
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Program terminated by user.{Style.RESET_ALL}")
