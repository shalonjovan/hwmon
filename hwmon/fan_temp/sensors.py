import os
from hwmon.fan_temp.resolver import find_hwmon_by_name
from hwmon.utils.fs import read_int, read_str


# -------- helpers --------

def _read_milli(path: str) -> float:
    return read_int(path) / 1000.0


# -------- BATTERY --------

def get_battery_info() -> dict:
    """
    Returns:
    {
        voltage: volts,
        power: watts,
        remaining: 0.0 - 1.0
    }
    """
    bat = find_hwmon_by_name("BAT0")

    voltage = read_int(f"{bat}/in0_input") / 1000.0
    power = read_int(f"{bat}/power1_input") / 1_000_000.0

    device = f"{bat}/device"
    full_design = read_int(f"{device}/energy_full_design")
    full_now = read_int(f"{device}/energy_full")

    remaining = (
        full_now / full_design
        if full_design > 0
        else 0.0
    )

    return {
        "voltage": voltage,
        "power": power,
        "battery life": f"{remaining*100:.1f}%",
    }


# -------- NVME --------

def get_nvme_temps() -> dict:
    """
    Returns:
    {
        label: temperature_in_celsius
    }
    """
    nvme = find_hwmon_by_name("nvme")
    temps = {}

    for fname in os.listdir(nvme):
        if not fname.startswith("temp") or not fname.endswith("_label"):
            continue

        idx = fname.replace("temp", "").replace("_label", "")
        label = read_str(f"{nvme}/{fname}")
        temp = _read_milli(f"{nvme}/temp{idx}_input")

        temps[label] = temp

    return temps


# -------- FANS --------

def get_fans() -> dict:
    """
    Returns:
    {
        fan_label: rpm
    }
    """
    asus = find_hwmon_by_name("asus")
    fans = {}

    for fname in os.listdir(asus):
        if not fname.startswith("fan") or not fname.endswith("_input"):
            continue

        idx = fname.replace("fan", "").replace("_input", "")
        rpm = read_int(f"{asus}/{fname}")
        label = read_str(f"{asus}/fan{idx}_label")

        fans[label] = rpm

    return fans
