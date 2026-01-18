from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from pathlib import Path

from hwmon.state.state import get_system_state
from hwmon.curves.curves import apply_profile


ASSETS = Path(__file__).parent / "assets"


def load_ascii(name: str) -> str:
    return (ASSETS / name).read_text()


def bar(value, max_value, width=20, char="█"):
    ratio = min(max(value / max_value, 0), 1)
    filled = int(ratio * width)
    return char * filled + " " * (width - filled)


class HwmonTUI(App):
    CSS_PATH = "tui.tcss"

    def compose(self) -> ComposeResult:
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
  Life : {state['battery']['battery life']}
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

        # -------- FANS --------
        fans_text = fan_ascii + "\n\n"
        for name, rpm in state["fans"].items():
            fans_text += (
                f"{name}: {rpm} RPM\n"
                f"[{bar(rpm, 7600)}]\n"
            )

        fans = Static(fans_text.strip(), id="fans")

        # -------- CPU + MEM (NOW BELOW FANS) --------
        cpu = state["cpu"]
        mem = state["memory"]

        cpu_mem = Static(
            f"""
CPU
  Temp: {cpu['temps']['package']}°C
  Usage: {cpu['usage_percent']:.1f}%
  [{bar(cpu['usage_percent'], 100)}]

Memory
  Used: {mem['usage']['used_mb']} MB
  Free: {mem['usage']['available_mb']} MB
  [{bar(mem['usage']['used_mb'], mem['total_mb'])}]
""",
            id="cpu_mem"
        )

        right = Vertical(
            fans,
            cpu_mem,
            id="right"
        )

        yield Vertical(
            Horizontal(left, right),
            Static("Curves applied: cpu | gpu | mid", id="footer")
        )


def main():
    HwmonTUI().run()


if __name__ == "__main__":
    main()
