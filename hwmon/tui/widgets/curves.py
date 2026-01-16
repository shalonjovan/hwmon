from textual.widgets import Static
from hwmon.curves.curves import load_profiles


class CurveBar(Static):
    def on_mount(self):
        profiles = load_profiles()
        names = " | ".join(profiles.keys())
        self.update(f"[b]Curves:[/b] {names}")
