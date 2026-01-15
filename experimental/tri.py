from textual.app import App
from textual.widgets import Static
from textual.events import MouseDown, MouseMove

class MouseDemo(App):
    def compose(self):
        yield Static("Click or move the mouse", id="box")

    def on_mouse_down(self, event: MouseDown) -> None:
        self.query_one("#box").update(
            f"Mouse down at x={event.x}, y={event.y}, button={event.button}"
        )

    def on_mouse_move(self, event: MouseMove) -> None:
        self.query_one("#box").update(
            f"Mouse move at x={event.x}, y={event.y}"
        )

MouseDemo().run()
