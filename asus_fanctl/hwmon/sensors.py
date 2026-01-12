# asus_fanctl/hwmon/sensors.py

import os
from asus_fanctl.hwmon.resolver import find_hwmon
from asus_fanctl.utils.fs import read_int

_CORETEMP = find_hwmon("coretemp")
_ASUS = find_hwmon("asus")


def _read_milli(path: str) -> float:
    return read_int(path) / 1000.0


# ---------- CPU PACKAGE ----------

def get_cpu_package():
    """
    Returns:
        {
          "label": "Package id 0",
          "temp": float,
          "crit": float
        }
    """
    label = read_file(os.path.join(_CORETEMP, "temp1_label")).strip()
    if label != "Package id 0":
        raise RuntimeError("temp1 is not CPU package")

    temp = _read_milli(os.path.join(_CORETEMP, "temp1_input"))
    crit = _read_milli(os.path.join(_CORETEMP, "temp1_crit"))

    return {
        "label": label,
        "temp": temp,
        "crit": crit,
    }


# ---------- CPU CORES ----------

def get_cpu_cores():
    """
    Returns:
        {
          core_number: {
            "temp": float,
            "crit": float
          }
        }
    """
    cores = {}

    for fname in os.listdir(_CORETEMP):
        if not fname.startswith("temp") or not fname.endswith("_label"):
            continue

        label_path = os.path.join(_CORETEMP, fname)
        label = open(label_path).read().strip()

        if not label.startswith("Core"):
            continue

        # Example: temp10_label -> temp10_input / temp10_crit
        idx = fname.replace("temp", "").replace("_label", "")
        core_no = int(label.replace("Core", "").strip())

        temp = _read_milli(os.path.join(_CORETEMP, f"temp{idx}_input"))
        crit = _read_milli(os.path.join(_CORETEMP, f"temp{idx}_crit"))

        cores[core_no] = {
            "temp": temp,
            "crit": crit,
        }

    return dict(sorted(cores.items()))


# ---------- FANS ----------

def get_all_fans():
    """
    Returns:
        {
          fan_id: {
            "label": str,
            "rpm": int
          }
        }
    """
    fans = {}

    for fname in os.listdir(_ASUS):
        if not fname.startswith("fan") or not fname.endswith("_input"):
            continue

        fan_id = int(fname.replace("fan", "").replace("_input", ""))
        rpm = read_int(os.path.join(_ASUS, fname))

        label_path = os.path.join(_ASUS, f"fan{fan_id}_label")
        label = open(label_path).read().strip() if os.path.exists(label_path) else "unknown"

        fans[fan_id] = {
            "label": label,
            "rpm": rpm,
        }

    return dict(sorted(fans.items()))


# ---------- small helper ----------
def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
