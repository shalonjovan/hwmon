from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Button
from textual.reactive import reactive
import time

from asus_fanctl.hwmon.sensors import (
    get_cpu_package,
    get_cpu_cores,
    get_all_fans,
    get_nvme_temps,
    get_battery_info,
)
from asus_fanctl.hwmon.curves import apply_curve
import json


CURVES_PATH = "asus_fanctl/config/curves.json"


class InfoBox(Static):
    pass


class CurveSelector(Static):
    selected = reactive(0)

    def __init__(self, curves: list[str]):
        super().__init__()
        self.curves = curves

    def render(self):
        buttons = []
        for i, name in enumerate(self.curves):
            if i == self.selected:
                buttons.append(f"[reverse]{name}[/reverse]")
            else:
                buttons.append(name)
        return "  ".join(buttons)

    def move_left(self):
        self.selected = (self.selected - 1) % len(self.curves)

    def move_right(self):
        self.selected = (self.selected + 1) % len(self.curves)

    def current(self):
        return self.curves[self.selected]


class FanCtlApp(App):
    CSS_PATH = "styles.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("left", "left", "Prev Curve"),
        ("right", "right", "Next Curve"),
        ("enter", "apply", "Apply Curve"),
    ]

    def __init__(self):
        super().__init__()
        with open(CURVES_PATH) as f:
            self.curves = json.load(f)
        self.curve_names = list(self.curves.keys())

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical():
            with Horizontal():
                self.cpu_box = InfoBox()
                self.gpu_box = InfoBox()
                yield self.cpu_box
                yield self.gpu_box

            self.fan_box = InfoBox()
            yield self.fan_box

            self.curve_selector = CurveSelector(self.curve_names)
            yield self.curve_selector

            self.misc_box = InfoBox()
            yield self.misc_box

        yield Footer()

    def on_mount(self):
        self.set_interval(1, self.refresh_stats)

    def refresh_stats(self):
        # CPU
        pkg = get_cpu_package()
        cores = get_cpu_cores()
        cpu_text = f"[b]CPU[/b]\n{pkg['temp']:.1f}°C\n"
        for c, d in cores.items():
            cpu_text += f"Core {c}: {d['temp']:.0f}°C  "
        self.cpu_box.update(cpu_text)

        # Fans
        fans = get_all_fans()
        fan_text = "[b]Fans[/b]\n"
        for f in fans.values():
            fan_text += f"{f['label']}: {f['rpm']} RPM\n"
        self.fan_box.update(fan_text)

        # NVMe + Battery
        nvme = get_nvme_temps()
        bat = get_battery_info()

        misc = "[b]NVMe[/b]\n"
        for t in nvme:
            misc += f"{t['label']}: {t['temp']:.0f}°C  "
        misc += "\n\n[b]Battery[/b]\n"
        misc += f"{bat['health']*100:.0f}%  {bat['voltage']:.1f}V  {bat['power']:.0f}W"

        self.misc_box.update(misc)

    def action_left(self):
        self.curve_selector.move_left()

    def action_right(self):
        self.curve_selector.move_right()

    def action_apply(self):
        name = self.curve_selector.current()
        cfg = self.curves[name]
        apply_curve(cfg["fan"], cfg["points"])

if __name__ == "__main__":
    FanCtlApp().run()
