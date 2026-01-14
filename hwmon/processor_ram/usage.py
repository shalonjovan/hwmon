import time
from hwmon.utils.proc import parse_meminfo


# ---------- CPU USAGE ----------

def _read_cpu_line() -> list[int]:
    """
    Returns cpu counters from /proc/stat 'cpu ' line.
    Order:
    user, nice, system, idle, iowait, irq, softirq, steal
    """
    with open("/proc/stat", "r") as f:
        for line in f:
            if line.startswith("cpu "):
                parts = line.split()
                return list(map(int, parts[1:9]))
    raise RuntimeError("cpu line not found in /proc/stat")


def get_cpu_usage_percent(interval: float = 1.0) -> float:
    """
    Returns total CPU usage percentage over `interval` seconds.
    """
    a = _read_cpu_line()
    time.sleep(interval)
    b = _read_cpu_line()

    total1 = sum(a)
    total2 = sum(b)

    idle1 = a[3] + a[4]   # idle + iowait
    idle2 = b[3] + b[4]

    diff_total = total2 - total1
    diff_idle = idle2 - idle1

    if diff_total <= 0:
        return 0.0

    usage = 100.0 * (diff_total - diff_idle) / diff_total
    return round(usage, 1)


# ---------- MEMORY USAGE ----------

def get_mem_usage() -> dict:
    """
    Returns:
    {
        total_mb,
        used_mb,
        available_mb,
        percent_used
    }
    """
    mem = parse_meminfo()

    total = mem["MemTotal"]
    available = mem["MemAvailable"]
    used = total - available

    percent = 100.0 * used / total if total > 0 else 0.0

    return {
        "total_mb": total // 1024,
        "used_mb": used // 1024,
        "available_mb": available // 1024,
        "percent_used": round(percent, 1),
    }
