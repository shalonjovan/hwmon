from textual.app import App
from .layout import MainLayout


class HwmonApp(App):
    CSS_PATH = "styles.tcss"

    def compose(self):
        yield MainLayout()


def main():
    HwmonApp().run()

if __name__ == "__main__":
    main()
