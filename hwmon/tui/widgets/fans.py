from textual.containers import Vertical
from textual.widgets import Static
from hwmon.state.state import get_system_state
from .ascii import AsciiArt


class FanPanel(Vertical):
    def __init__(self, ascii_path: str, **kwargs):
        super().__init__(**kwargs)
        self.ascii_path = ascii_path

    def compose(self):
        yield AsciiArt(self.ascii_path)
        yield Static(self._fan_text())

    def _fan_text(self) -> str:
        s = get_system_state()
        txt = ""

        for fan, rpm in s["fans"].items():
            txt += f"{fan}: {rpm} RPM\n"

        return txt.strip()
