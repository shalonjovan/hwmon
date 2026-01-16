from textual.widgets import Static
from hwmon.state.state import get_system_state


class CpuMemPanel(Static):
    def on_mount(self):
        self.refresh()

    def update_panel(self):
        s = get_system_state()

        cpu = s["cpu"]
        mem = s["memory"]

        txt = f"""
CPU
  Temp: {cpu['temps']['package']}°C
  Usage: {cpu['usage_percent']}%

Memory
  Total: {mem['total_mb']} MB
  Used: {mem['usage']['used_mb']} MB
  Free: {mem['usage']['available_mb']} MB
"""
        self.update(txt)
