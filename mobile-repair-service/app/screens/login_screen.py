from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def show_password(self):
        if self.ids.password_icon.icon == 'eye':
            self.ids.password_icon.icon = 'eye-off'
            self.ids.password_input.password = False
        else:
            self.ids.password_icon.icon = 'eye'
            self.ids.password_input.password = True
