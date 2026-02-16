import time
from pathlib import Path
from typing import Dict, Any

import psutil
import sensors

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

        # --- Network tracking ---
        self._last_net = psutil.net_io_counters()
        self._last_net_time = time.time()

        # Prime cpu_percent to avoid initial 0 spike
        psutil.cpu_percent(interval=None)

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

    def network(self) -> Dict[str, Any]:
        current = psutil.net_io_counters()
        now = time.time()

        elapsed = now - self._last_net_time
        if elapsed <= 0:
            elapsed = 1

        upload_speed = (current.bytes_sent - self._last_net.bytes_sent) / elapsed
        download_speed = (current.bytes_recv - self._last_net.bytes_recv) / elapsed

        self._last_net = current
        self._last_net_time = now

        return {
            "bytes_sent": current.bytes_sent,
            "bytes_recv": current.bytes_recv,
            "upload_speed": upload_speed,
            "download_speed": download_speed,
        }

    def _parse_sensors(self):
        cpu_temp = None
        nvme_temps = {}
        fans = {}
        batteries = []
        misc_temps = {}

        for chip in sensors.iter_detected_chips():
            chip_name = str(chip).lower()
            battery_data = {}

            for feature in chip:
                label = feature.label
                value = feature.get_value()
                ftype = feature.type

                if ftype == 2:
                    if "package" in label.lower():
                        cpu_temp = value
                    elif "nvme" in chip_name:
                        nvme_temps[f"{chip_name}:{label}"] = value
                    else:
                        misc_temps[label] = value

                elif ftype == 1:
                    fans[label] = int(value)

                elif ftype == 0:
                    if "bat" in chip_name:
                        battery_data["voltage"] = round(value, 2)

                elif ftype == 3:
                    if "bat" in chip_name:
                        battery_data["power"] = round(value, 2)

            if battery_data:
                batteries.append(battery_data)

        return cpu_temp, nvme_temps, fans, batteries, misc_temps

    def gpu(self) -> Dict[str, Any]:
        if not NVML_AVAILABLE:
            return {}

        gpus = {}
        try:
            count = pynvml.nvmlDeviceGetCount()
            for i in range(count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(name, bytes):
                    name = name.decode()

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

    def snapshot(self) -> Dict[str, Any]:
        cpu_temp, nvme_temps, fans, batteries, misc_temps = self._parse_sensors()

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
            "network": self.network(),
            "nvme": nvme_temps,
            "fans": fans,
            "batteries": batteries,
            "misc_temps": misc_temps,
            "gpu": self.gpu(),
        }

    def cleanup(self):
        sensors.cleanup()
