import time
from pathlib import Path
from typing import Dict, Any

import psutil
import sensors

# NVML is optional; tool still works without NVIDIA GPU
try:
    import pynvml
    pynvml.nvmlInit()
    NVML_AVAILABLE = True
except Exception:
    NVML_AVAILABLE = False


class SystemState:

    def __init__(self):
        sensors.init()
        self.product_name = self._get_product_name()

    def _get_product_name(self) -> str:
        try:
            return Path("/sys/class/dmi/id/product_name").read_text().strip()
        except Exception:
            return "Unknown System"

    def cpu(self) -> Dict[str, Any]:
        return {
            "usage_percent": psutil.cpu_percent(interval=None),
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
        }

    def memory(self) -> Dict[str, Any]:
        mem = psutil.virtual_memory()
        return {
            "total_mb": mem.total // (1024 * 1024),
            "used_mb": mem.used // (1024 * 1024),
            "available_mb": mem.available // (1024 * 1024),
            "percent_used": mem.percent,
        }

    # Centralized sensor parsing using pysensors
    def _parse_sensors(self):
        cpu_temp = None
        nvme_temps = {}
        fans = {}
        battery = {}
        misc_temps = {}

        for chip in sensors.iter_detected_chips():
            chip_name = str(chip).lower()

            for feature in chip:
                label = feature.label
                value = feature.get_value()

                if "coretemp" in chip_name:
                    if label == "Package id 0":
                        cpu_temp = value
                    elif label.startswith("Core"):
                        misc_temps[label] = value

                elif "nvme" in chip_name:
                    nvme_temps[label] = value

                elif "asus" in chip_name and "fan" in label:
                    fans[label] = int(value)

                elif "bat" in chip_name:
                    if label.startswith("in"):
                        battery["voltage"] = round(value, 2)
                    elif label.startswith("power"):
                        battery["power"] = round(value, 2)

                elif "acpi" in chip_name:
                    misc_temps[label] = value

        return cpu_temp, nvme_temps, fans, battery, misc_temps

    def gpu(self) -> Dict[str, Any]:
        if not NVML_AVAILABLE:
            return {}

        gpus = {}
        try:
            count = pynvml.nvmlDeviceGetCount()
            for i in range(count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                temp = pynvml.nvmlDeviceGetTemperature(
                    handle,
                    pynvml.NVML_TEMPERATURE_GPU
                )

                gpus[name] = {
                    "usage_percent": util.gpu,
                    "temp": temp,
                    "mem_used_mb": mem.used // (1024 * 1024),
                    "mem_total_mb": mem.total // (1024 * 1024),
                }
        except Exception:
            pass

        return gpus

    # Single snapshot used by the TUI layer
    def snapshot(self) -> Dict[str, Any]:
        cpu_temp, nvme_temps, fans, battery, misc_temps = self._parse_sensors()

        return {
            "timestamp": time.time(),
            "system": {
                "product_name": self.product_name,
            },
            "cpu": {
                **self.cpu(),
                "temp": cpu_temp,
            },
            "memory": self.memory(),
            "nvme": nvme_temps,
            "fans": fans,
            "battery": battery,
            "misc_temps": misc_temps,
            "gpu": self.gpu(),
        }

    def cleanup(self):
        sensors.cleanup()
