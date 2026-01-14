def parse_cpuinfo() -> dict:
    info = {}
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if not line.strip():
                break
            if ":" in line:
                k, v = line.split(":", 1)
                info[k.strip()] = v.strip()
    return info


def parse_meminfo() -> dict:
    mem = {}
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if ":" in line:
                k, v = line.split(":", 1)
                mem[k.strip()] = int(v.strip().split()[0])
    return mem
