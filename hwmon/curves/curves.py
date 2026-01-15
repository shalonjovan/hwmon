import os
import json
import subprocess

from hwmon.fan_temp.resolver import find_hwmon_by_name
from hwmon.utils.fs import read_int


_CURVE = find_hwmon_by_name("asus_custom_fan_curve")
_CURVES_JSON = os.path.join(
    os.path.dirname(__file__),
    "curves.json"
)


# ---------- low-level write ----------

def _write_sysfs(path: str, value: int):
    """
    Write to sysfs using tee (EC-safe).
    """
    cmd = f"echo {value} | tee {path} > /dev/null"
    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to write {value} to {path}")


# ---------- pwm control ----------

def enable_pwm(fan: int):
    path = os.path.join(_CURVE, f"pwm{fan}_enable")
    _write_sysfs(path, 1)

    # verify
    if read_int(path) != 1:
        raise RuntimeError(f"PWM enable failed for fan {fan}")


def disable_pwm(fan: int):
    _write_sysfs(os.path.join(_CURVE, f"pwm{fan}_enable"), 0)


# ---------- curve writing ----------

def write_curve_point(fan: int, point: int, temp_c: int, pwm: int):
    _write_sysfs(
        os.path.join(_CURVE, f"pwm{fan}_auto_point{point}_temp"),
        temp_c
    )
    _write_sysfs(
        os.path.join(_CURVE, f"pwm{fan}_auto_point{point}_pwm"),
        pwm
    )


def apply_curve(fan: int, points: list[list[int]]):
    """
    Apply curve safely (EC ordering).
    """
    for idx, (temp, pwm) in enumerate(points, start=1):
        write_curve_point(fan, idx, temp, pwm)

    # MUST enable AFTER writing points
    enable_pwm(fan)


# ---------- profiles ----------

def load_profiles() -> dict:
    with open(_CURVES_JSON, "r") as f:
        return json.load(f)


def apply_profile(name: str):
    """
    Apply a named curve profile (cpu / gpu / mid).
    """
    profiles = load_profiles()

    if name not in profiles:
        raise ValueError(f"Unknown curve profile: {name}")

    profile = profiles[name]
    apply_curve(profile["fan"], profile["points"])
