"""Small, read-only system telemetry helpers."""
import platform
import psutil


def get_system_status() -> str:
    cpu = psutil.cpu_percent(interval=0.25)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    parts = [
        f"OS: {platform.system()} {platform.release()}",
        f"CPU: {cpu:.0f}%",
        f"RAM: {memory.percent:.0f}% ({memory.used / (1024**3):.1f}/{memory.total / (1024**3):.1f} GB)",
        f"Disk: {disk.percent:.0f}% used",
    ]
    try:
        battery = psutil.sensors_battery()
        if battery:
            parts.append(f"Battery: {battery.percent:.0f}%" + (" (charging)" if battery.power_plugged else ""))
    except (AttributeError, OSError):
        pass
    return " | ".join(parts)


def get_telemetry_line() -> str:
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return f"CPU {cpu:.0f}%   •   RAM {memory:.0f}%   •   DISK {disk:.0f}%"
