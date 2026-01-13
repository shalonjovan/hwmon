import json
import time

from asus_fanctl.hwmon.sensors import (
    get_cpu_package,
    get_cpu_cores,
    get_all_fans,
    get_nvme_temps,
    get_battery_info,
)

from asus_fanctl.hwmon.curves import apply_curve


CURVES_PATH = "asus_fanctl/config/curves.json"


def display_monitors():
    pkg = get_cpu_package()
    cores = get_cpu_cores()
    nvme = get_nvme_temps()
    fans = get_all_fans()
    battery = get_battery_info()

    print("coretemp-isa-0000")
    print("Adapter: ISA adapter")
    print(
        f"{pkg['label']}:  +{pkg['temp']:.1f}°C  "
        f"(high = +{pkg['crit']:.1f}°C, crit = +{pkg['crit']:.1f}°C)"
    )

    for core, data in cores.items():
        print(
            f"Core {core:<2}:      +{data['temp']:.1f}°C  "
            f"(high = +{data['crit']:.1f}°C, crit = +{data['crit']:.1f}°C)"
        )

    print("\nNVMe:")
    for t in nvme:
        print(f"  {t['label']}: +{t['temp']:.1f}°C")

    print("\nFans:")
    for _, fan in fans.items():
        print(f"  {fan['label']}: {fan['rpm']} RPM")

    print("\nBattery:")
    print(f"  Voltage: {battery['voltage']:.2f} V")
    print(f"  Power:   {battery['power']:.2f} W")
    print(f"  Health:  {battery['health'] * 100:.1f} %")


def apply_curves():
    with open(CURVES_PATH) as f:
        curves = json.load(f)

    for name, cfg in curves.items():
        print(f"Applying {name} curve...")
        apply_curve(cfg["fan"], cfg["points"])

    print("✓ All curves applied\n")


def main():
    apply_curves()

    try:
        while True:
            print("\033[H\033[J", end="")  
            display_monitors()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting monitor mode.")


if __name__ == "__main__":
    main()
