# hwmon/model/cpu_info.py

from hwmon.utils.proc import parse_cpuinfo


def get_cpu_info() -> dict:
    cpu = parse_cpuinfo()

    return {
        "vendor": cpu.get("vendor_id", ""),
        "model_name": cpu.get("model name", ""),
        "family": cpu.get("cpu family", ""),
        "model": cpu.get("model", ""),
        "stepping": cpu.get("stepping", ""),
        "cores": int(cpu.get("cpu cores", 0)),
        "siblings": int(cpu.get("siblings", 0)),
        "cache_kb": cpu.get("cache size", "").replace(" KB", ""),
        "architecture": "x86_64",  # implied for your system
    }
