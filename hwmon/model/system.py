# hwmon/model/system.py

from hwmon.utils.fs import read_str

DMI = "/sys/class/dmi/id"


def get_system_info() -> dict:
    """
    Returns laptop / motherboard identity info.
    """
    return {
        "vendor": read_str(f"{DMI}/sys_vendor"),
        "product_name": read_str(f"{DMI}/product_name"),
        "product_version": read_str(f"{DMI}/product_version"),
        "product_family": read_str(f"{DMI}/product_family"),
        "board_name": read_str(f"{DMI}/board_name"),
        "board_vendor": read_str(f"{DMI}/board_vendor"),
        "bios_vendor": read_str(f"{DMI}/bios_vendor"),
        "bios_version": read_str(f"{DMI}/bios_version"),
        "bios_date": read_str(f"{DMI}/bios_date"),
    }
