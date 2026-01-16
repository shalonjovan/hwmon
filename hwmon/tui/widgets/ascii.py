from textual.widgets import Static
from pathlib import Path


class AsciiArt(Static):
    DEFAULT_CSS = """
    AsciiArt {
        height: 1fr;
    }
    """

    def __init__(self, path: str, **kwargs):
        self.path = Path(path)
        self.raw_lines = []
        super().__init__("", **kwargs)

    def on_mount(self):
        self.raw_lines = self.path.read_text().splitlines()
        self.update_scaled()

    def on_resize(self):
        self.update_scaled()

    def update_scaled(self):
        if not self.raw_lines or self.size.height == 0:
            return

        max_w = self.size.width
        max_h = self.size.height

        src_h = len(self.raw_lines)
        src_w = max(len(line) for line in self.raw_lines)

        y_step = max(1, src_h // max_h)
        x_step = max(1, src_w // max_w)

        scaled = []
        for y in range(0, src_h, y_step):
            line = self.raw_lines[y]
            scaled.append(line[::x_step][:max_w])
            if len(scaled) >= max_h:
                break

        self.update("\n".join(scaled))
