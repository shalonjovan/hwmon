from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from pathlib import Path

from state import SystemState

ASSETS = Path(__file__).parent / "assets"


def load_ascii(name: str) -> str:
    return (ASSETS / name).read_text()


def bar(value, max_value, width=20, char="█"):
    ratio = min(max(value / max_value, 0), 1)
    filled = int(ratio * width)
    return char * filled + " " * (width - filled)


class HwmonTUI(App):
    CSS_PATH = "tui.tcss"

    def on_mount(self):
        self.state = SystemState()
        self.set_interval(1, self.refresh_state)

    def compose(self) -> ComposeResult:
        pc_ascii = load_ascii("pc.txt")

        self.pc_ascii = Static(pc_ascii, id="pc_ascii")
        self.system_info = Static("", id="system_info")
        self.fans = Static("", id="fans")
        self.cpu_mem = Static("", id="cpu_mem")

        left = Vertical(self.pc_ascii, self.system_info, id="left")
        right = Vertical(self.fans, self.cpu_mem, id="right")

        yield Vertical(
            Horizontal(left, right),
            Static("Monitoring with pysensors + psutil + nvml", id="footer")
        )

    # UI layer only formats snapshot data
    def refresh_state(self):
        state = self.state.snapshot()

        battery = state["battery"]
        nvme = state["nvme"]

        left_text = f"""
[b]{state['system']['product_name']}[/b]
"""

        if battery:
            left_text += f"""
Battery:
  {battery.get('voltage', 0)} V
  {battery.get('power', 0)} W
"""

        if nvme:
            left_text += "\nNVMe:\n"
            for label, temp in nvme.items():
                left_text += f"  {label}: {temp:.1f}°C\n"

        self.system_info.update(left_text.strip())

        cpu = state["cpu"]
        mem = state["memory"]

        right_text = f"""
CPU
  Temp: {cpu.get('temp', 0):.1f}°C
  Usage: {cpu['usage_percent']}%
  [{bar(cpu['usage_percent'], 100)}]

Memory
  Used: {mem['used_mb']} MB
  Free: {mem['available_mb']} MB
  [{bar(mem['percent_used'], 100)}]
"""

        if state["gpu"]:
            right_text += "\nGPU\n"
            for name, info in state["gpu"].items():
                right_text += (
                    f"  {name}\n"
                    f"    Usage: {info['usage_percent']}%\n"
                    f"    Temp: {info['temp']}°C\n"
                )

        self.cpu_mem.update(right_text.strip())

        fan_ascii = load_ascii("fan.txt")
        fans_text = fan_ascii + "\n\n"

        for name, rpm in state["fans"].items():
            fans_text += (
                f"{name}: {rpm} RPM\n"
                f"[{bar(rpm, 7600)}]\n"
            )

        self.fans.update(fans_text.strip())


def main():
    HwmonTUI().run()


if __name__ == "__main__":
    main()
