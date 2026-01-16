from textual.containers import Horizontal, Vertical
from textual.widget import Widget

from .widgets.ascii import AsciiArt
from .widgets.system import SystemPanel
from .widgets.cpu_mem import CpuMemPanel
from .widgets.fans import FanPanel
from .widgets.curves import CurveBar


class MainLayout(Widget):
    def compose(self):
        yield Horizontal(
            Vertical(
                AsciiArt("hwmon/tui/assets/pc.txt"),
                SystemPanel(),
                id="left"
            ),
            Vertical(
                Horizontal(
                    CpuMemPanel(),
                    FanPanel("hwmon/tui/assets/fan.txt"),
                ),
                id="right"
            )
        )
        yield CurveBar()
