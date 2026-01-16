from textual.widgets import Static
from hwmon.state.state import get_system_state


class SystemPanel(Static):
    def on_mount(self):
        self.update_panel()

    def update_panel(self):
        s = get_system_state()
        bat = s["battery"]

        txt = f"""
[b]{s['system']['product_name']}[/b]

Battery:
  Life: {bat.get("battery life", "N/A")}
  Voltage: {bat.get("voltage", 0)} V
  Power: {bat.get("power", 0)} W

NVMe:
"""

        for label, temp in s["nvme"].items():
            txt += f"  {label}: {temp:.1f}°C\n"

        self.update(txt.strip())
