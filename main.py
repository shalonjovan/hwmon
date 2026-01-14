# hwmon/main.py

from hwmon.model.system import get_system_info
from hwmon.model.cpu_info import get_cpu_info
from hwmon.utils.proc import parse_meminfo
import pprint


def main():
    print("SYSTEM INFO")
    pprint.pprint(get_system_info())

    print("\nCPU INFO")
    pprint.pprint(get_cpu_info())

    print("\nMEMORY INFO (raw)")
    mem = parse_meminfo()
    for k in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
        print(f"{k}: {mem[k]} kB")


if __name__ == "__main__":
    main()
