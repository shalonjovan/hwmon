# hwmon/utils/proc.py

def parse_cpuinfo() -> dict:
    """
    Parses /proc/cpuinfo and returns only first processor's info.
    """
    info = {}
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if not line.strip():
                break  # stop after first processor
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    return info


def parse_meminfo() -> dict:
    """
    Parses /proc/meminfo into {key: value_kB}
    """
    mem = {}
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if ":" not in line:
                continue
            key, rest = line.split(":", 1)
            value = rest.strip().split()[0]
            mem[key] = int(value)
    return mem
