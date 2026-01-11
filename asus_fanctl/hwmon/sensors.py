
import os
from asus_fanctl.hwmon.resolver import find_hwmon
from asus_fanctl.utils.fs import read_int

_CORETEMP = find_hwmon("coretemp")
_ASUS = find_hwmon("asus")


def get_cpu_temp() -> float:
    """
    Returns CPU temperature in °C
    """
    for fname in os.listdir(_CORETEMP):
        if fname.startswith("temp") and fname.endswith("_input"):
            milli = read_int(os.path.join(_CORETEMP, fname))
            return milli / 1000.0
    raise RuntimeError("CPU temperature sensor not found")


def get_fan_rpm(fan_id: int) -> int:
    """
    fan_id starts from 1
    """
    path = os.path.join(_ASUS, f"fan{fan_id}_input")
    return read_int(path)


def get_all_fans() -> dict[int, int]:
    """
    Returns {fan_id: rpm}
    """
    fans = {}
    for fname in os.listdir(_ASUS):
        if fname.startswith("fan") and fname.endswith("_input"):
            fan_id = int(fname.replace("fan", "").replace("_input", ""))
            fans[fan_id] = read_int(os.path.join(_ASUS, fname))
    return fans
