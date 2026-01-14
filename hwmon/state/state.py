import time

from hwmon.model.info import (
    get_system_product_name,
    get_cpu_info,
    get_total_ram_mb,
)

from hwmon.fan_temp.sensors import (
    get_cpu_temps,
    get_nvme_temps,
    get_fans,
    get_battery_info,
)

from hwmon.processor_ram.usage import (
    get_cpu_usage_percent,
    get_mem_usage,
)


def get_system_state(interval: float = 1.0) -> dict:
    """
    Returns a full snapshot of system state.
    """
    cpu_info = get_cpu_info()
    mem_usage = get_mem_usage()

    return {
        "meta": {
            "timestamp": time.time(),
        },

        "system": {
            "product_name": get_system_product_name(),
        },

        "cpu": {
            "info": cpu_info,
            "usage_percent": get_cpu_usage_percent(interval),
            "temps": get_cpu_temps(),
        },

        "memory": {
            "total_mb": get_total_ram_mb(),
            "usage": mem_usage,
        },

        "fans": get_fans(),

        "nvme": get_nvme_temps(),

        "battery": get_battery_info(),
    }
