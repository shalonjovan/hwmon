
import os
HWMON_BASE = "/sys/class/hwmon"


def find_hwmon(name: str) -> str:
    for hw in os.listdir(HWMON_BASE):
        path = os.path.join(HWMON_BASE, hw)
        try:
            with open(os.path.join(path, "name"), "r") as f:
                if f.read().strip() == name:
                    return path
        except Exception:
            continue
    raise RuntimeError(f"hwmon device '{name}' not found")


def get_all_hwmons() -> dict[str, str]:
    result = {}
    for hw in os.listdir(HWMON_BASE):
        path = os.path.join(HWMON_BASE, hw)
        try:
            with open(os.path.join(path, "name"), "r") as f:
                result[f.read().strip()] = path
        except Exception:
            continue
    return result

