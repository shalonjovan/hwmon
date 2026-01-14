from hwmon.fan_temp.sensors import (
    get_battery_info,
    get_nvme_temps,
    get_fans,
)


def main():
    print("Battery:")
    print(get_battery_info())

    print("\nNVMe Temps:")
    for k, v in get_nvme_temps().items():
        print(f"  {k}: {v:.1f}°C")

    print("\nFans:")
    for k, v in get_fans().items():
        print(f"  {k}: {v} RPM")


if __name__ == "__main__":
    main()
