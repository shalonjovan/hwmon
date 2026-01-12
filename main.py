# main.py

from asus_fanctl.hwmon.sensors import (
    get_cpu_package,
    get_cpu_cores,
    get_all_fans,
)


def main():
    pkg = get_cpu_package()
    cores = get_cpu_cores()
    fans = get_all_fans()

    print("coretemp-isa-0000")
    print("Adapter: ISA adapter")
    print(
        f"{pkg['label']}:  +{pkg['temp']:.1f}°C  "
        f"(high = +{pkg['crit']:.1f}°C, crit = +{pkg['crit']:.1f}°C)"
    )

    for core, data in cores.items():
        print(
            f"Core {core}:        +{data['temp']:.1f}°C  "
            f"(high = +{data['crit']:.1f}°C, crit = +{data['crit']:.1f}°C)"
        )

    print()
    for fan_id, fan in fans.items():
        print(f"{fan['label']}: {fan['rpm']} RPM")


if __name__ == "__main__":
    main()
