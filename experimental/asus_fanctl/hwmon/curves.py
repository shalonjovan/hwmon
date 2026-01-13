import os
import json
from asus_fanctl.hwmon.resolver import find_hwmon
from asus_fanctl.utils.fs import read_int

_CURVE = find_hwmon("asus_custom_fan_curve")


import subprocess


def _write_sysfs(path: str, value: int):
    """
    Write to sysfs using tee to ensure kernel driver accepts it.
    """
    cmd = f"echo {value} | sudo tee {path} > /dev/null"
    result = subprocess.run(
        cmd,
        shell=True,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to write {value} to {path}")



def enable_pwm(fan: int):
    path = os.path.join(_CURVE, f"pwm{fan}_enable")
    _write_sysfs(path, 1)

    # verify
    current = read_int(path)
    if current != 1:
        raise RuntimeError(
            f"Failed to enable PWM for fan {fan}, got {current}"
        )


def disable_pwm(fan: int):
    _write_sysfs(os.path.join(_CURVE, f"pwm{fan}_enable"), 0)


def write_curve_point(fan: int, point: int, temp_c: int, pwm: int):
    temp_path = os.path.join(
        _CURVE, f"pwm{fan}_auto_point{point}_temp"
    )
    pwm_path = os.path.join(
        _CURVE, f"pwm{fan}_auto_point{point}_pwm"
    )

    _write_sysfs(temp_path, temp_c)
    _write_sysfs(pwm_path, pwm)


def apply_curve(fan: int, points: list[list[int]]):

    for idx, (temp, pwm) in enumerate(points, start=1):
        write_curve_point(fan, idx, temp, pwm)

    enable_pwm(fan)

    path = os.path.join(_CURVE, f"pwm{fan}_enable")
    current = read_int(path)
    if current != 1:
        raise RuntimeError(
            f"EC override detected: pwm{fan}_enable = {current}"
        )
