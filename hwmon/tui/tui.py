from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from pathlib import Path

from hwmon.state.state import get_system_state
from hwmon.curves.curves import apply_profile


ASSETS = Path(__file__).parent / "assets"


def load_ascii(name: str) -> str:
    return (ASSETS / name).read_text()


class HwmonTUI(App):
    CSS_PATH = "tui.tcss"

    def compose(self) -> ComposeResult:
        # 🔥 APPLY CURVES ON STARTUP (ONE TIME)
        apply_profile("cpu")
        apply_profile("gpu")
        apply_profile("mid")

        state = get_system_state()

        pc_ascii = load_ascii("pc.txt")
        fan_ascii = load_ascii("fan.txt")

        # -------- LEFT PANEL --------
        left = Vertical(
            Static(pc_ascii, id="pc_ascii"),

            Static(
                f"""
[b]{state['system']['product_name']}[/b]

Battery:
  {state['battery']['battery life']}
  {state['battery']['voltage']} V
  {state['battery']['power']} W

NVMe:
""" + "\n".join(
                    f"  {k}: {v:.1f}°C"
                    for k, v in state["nvme"].items()
                ),
                id="system_info"
            ),
            id="left"
        )

        # -------- CPU + MEM --------
        cpu = state["cpu"]
        mem = state["memory"]

        cpu_mem = Static(
            f"""
CPU
  Temp: {cpu['temps']['package']}°C
  Usage: {cpu['usage_percent']}%

Memory
  Total: {mem['total_mb']} MB
  Used: {mem['usage']['used_mb']} MB
  Free: {mem['usage']['available_mb']} MB
""",
            id="cpu_mem"
        )

        # -------- FANS --------
        fans = Static(
            fan_ascii + "\n\n" +
            "\n".join(
                f"{k}: {v} RPM"
                for k, v in state["fans"].items()
            ),
            id="fans"
        )

        right = Horizontal(cpu_mem, fans, id="right")

        yield Vertical(
            Horizontal(left, right),
            Static("Curves applied: cpu | gpu | mid", id="footer")
        )


def main():
    HwmonTUI().run()


if __name__ == "__main__":
    main()
