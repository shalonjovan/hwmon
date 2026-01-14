import os
from hwmon.utils.fs import read_str

HWMON_BASE = "/sys/class/hwmon"


def find_hwmon_by_name(target: str) -> str:
    """
    Resolve hwmon path by its 'name' file.
    Example: BAT0, nvme, asus
    """
    for hw in os.listdir(HWMON_BASE):
        path = f"{HWMON_BASE}/{hw}"
        name = read_str(f"{path}/name")
        if name == target:
            return path
    raise RuntimeError(f"hwmon device '{target}' not found")
