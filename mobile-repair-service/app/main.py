import logging

from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles

from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen

from utils.database_utils import check_database_connection


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__()
        self.sm = ScreenManager()

    def build(self):
        # self.theme_cls.theme_style_switch_animation = True
        # ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.accent_palette = 'BlueGray'
        self.theme_cls.primary_hue = '900'
        self.theme_cls.material_style = 'M3'

        LabelBase.register(
            name="JetBrainsMono",
            fn_regular="media/fonts/JetBrainsMono/ttf/JetBrainsMono-Regular.ttf",
            fn_bold="media/fonts/JetBrainsMono/ttf/JetBrainsMono-Bold.ttf",
            fn_italic="media/fonts/JetBrainsMono/ttf/JetBrainsMono-Italic.ttf",
        )

        theme_font_styles.append("JetBrainsMono")
        self.theme_cls.font_styles["JetBrainsMono"] = [
            "JetBrainsMono",
            16,
            False,
            0.15
        ]

        # Load screen definitions from .kv files
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/home_screen.kv")

        # self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login_screen'))
        self.sm.add_widget(HomeScreen(name='home_screen'))

        return self.sm

    def on_start(self) -> None:
        logging.info('MainApp: Application started!')
        check_database_connection()

    def on_stop(self) -> None:
        logging.info('MainApp: Application stopped!')


if __name__ == '__main__':
    MainApp().run()
