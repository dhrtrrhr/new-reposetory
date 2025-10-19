# school_clicker.py
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.resources import resource_find
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image


# Розмір вікна (як у презентації — зручно на ПК; на Android не впливає)
Window.size = (450, 800)


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="menu", **kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Картинка у верхній частині меню (вбудована іконка Kivy — щоб не шукати файл)
        icon = resource_find("data/logo/kivy-icon-256.png") or ""
        img_title = Image(source=icon, size_hint=(1, 0.5))
        layout.add_widget(img_title)

        # Текстовий заголовок
        lbl_title = Label(text="Main Menu", font_size="40sp", size_hint=(1, 0.2))
        layout.add_widget(lbl_title)

        # Кнопка Play
        btn_play = Button(text="PLAY", size_hint=(1, 0.15), font_size="20sp")
        btn_play.bind(on_press=self.go_game)
        layout.add_widget(btn_play)

        # Кнопка Settings
        btn_settings = Button(text="SETTINGS", size_hint=(1, 0.15), font_size="20sp")
        btn_settings.bind(on_press=self.go_settings)
        layout.add_widget(btn_settings)

        # Кнопка Exit
        btn_exit = Button(text="EXIT", size_hint=(1, 0.15), font_size="20sp")
        btn_exit.bind(on_press=self.exit_app)
        layout.add_widget(btn_exit)

        self.add_widget(layout)

    # Перехід до екрана гри
    def go_game(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "game"

    # Перехід до екрана налаштувань
    def go_settings(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "settings"

    # Вихід з програми (надійніше — через поточний App)
    def exit_app(self, *args):
        App.get_running_app().stop()


class Game(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="game", **kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Надпис "Game Screen"
        self.lbl_game = Label(text="Game Screen", font_size="40sp", size_hint=(1, 0.25))
        layout.add_widget(self.lbl_game)

        # Лічильник кліків
        self.counter_label = Label(text="Кліки: 0", font_size="28sp", size_hint=(1, 0.2))
        layout.add_widget(self.counter_label)

        # Кнопка кліку (власне “клікер”)
        btn_click = Button(text="КЛІК!", size_hint=(1, 0.3), font_size="28sp")
        btn_click.bind(on_press=self.on_click)
        layout.add_widget(btn_click)

        # Кнопка повернення
        btn_back = Button(text="Back to Menu", size_hint=(1, 0.2), font_size="20sp")
        btn_back.bind(on_press=self.go_menu)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        # Підтягнути поточний лічильник із застосунку
        app = App.get_running_app()
        self.counter_label.text = f"Кліки: {app.count}"

    def on_click(self, *args):
        app = App.get_running_app()
        app.count += app.step
        self.counter_label.text = f"Кліки: {app.count}"

    # Повернення до меню
    def go_menu(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "menu"


class Settings(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="settings", **kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        lbl_settings = Label(text="Settings", font_size="40sp", size_hint=(1, 0.6))
        layout.add_widget(lbl_settings)

        btn_back = Button(text="Back to Menu", size_hint=(1, 0.2), font_size="20sp")
        btn_back.bind(on_press=self.go_menu)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Повернення до меню
    def go_menu(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "menu"



class MediumApp(App):
    # назву лишив як у слайдах; можна перейменувати на ClickerApp
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0  # лічильник кліків
        self.step = 1   # приріст за один клік

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu())
        sm.add_widget(Game())
        sm.add_widget(Settings())
        return sm


if __name__ == "__main__":
    MediumApp().run()
