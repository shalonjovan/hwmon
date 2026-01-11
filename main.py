
from asus_fanctl.hwmon.sensors import (
    get_cpu_temp,
    get_all_fans,
)


def main():
    cpu_temp = get_cpu_temp()
    fans = get_all_fans()

    print(f"CPU Temp: {cpu_temp:.1f} °C")
    for fan, rpm in fans.items():
        print(f"Fan {fan}: {rpm} RPM")


if __name__ == "__main__":
    main()
