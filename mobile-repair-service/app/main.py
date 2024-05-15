import logging

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__()
        self.sm = ScreenManager()

    def build(self):
        # self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Indigo'


        # Load screen definitions from .kv files
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/home_screen.kv")

        # self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login_screen'))
        self.sm.add_widget(HomeScreen(name='home_screen'))

        return self.sm

    def on_start(self) -> None:
        logging.info('MainApp: Application started!')

    def on_stop(self) -> None:
        logging.info('MainApp: Application stopped!')


if __name__ == '__main__':
    MainApp().run()
