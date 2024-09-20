import matplotlib.pyplot as plt
import datetime

SYSTEM_METRICS_FILE = 'system_metrics.txt'

def plot_system_metrics():
    # Lists to store the data
    timestamps = []
    cpu_usages = []
    memory_usages = []

    # Read the file and parse the data
    try:
        with open(SYSTEM_METRICS_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    timestamp, cpu_usage, memory_usage = parts
                    timestamps.append(datetime.datetime.fromtimestamp(float(timestamp)))
                    cpu_usages.append(float(cpu_usage))
                    memory_usages.append(float(memory_usage))
    except Exception as e:
        print(f"Error reading file: {e}")

    # Plotting the data
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(timestamps, cpu_usages, label='CPU Usage (%)', color='blue')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(timestamps, memory_usages, label='Memory Usage (%)', color='green')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.title('Memory Usage Over Time')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_system_metrics()
