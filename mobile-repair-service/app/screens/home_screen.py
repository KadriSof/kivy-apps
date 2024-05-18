from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, ThreeLineIconListItem, ThreeLineAvatarIconListItem, IconRightWidget, \
    IconLeftWidget


class HomeScreen(Screen):

    def on_enter(self, *args):
        for i in range(15):
            #self.ids.pending_container.add_widget(Button(text=f"button {i}", size_hint_y=None, height=100))
            self.ids.pending_container.add_widget(
                DeviceItem(
                    device_name=f"Device n° {i}",
                    device_brand="IPhone",
                    device_status="pending",
                    size_hint_y=None,
                ))
    def test_button(self):
        for widget_id in self.ids:
            print(widget_id, ':', self.ids[widget_id].text)


class DeviceItem(MDBoxLayout):
    device_name = StringProperty()
    device_brand = StringProperty()
    device_status = StringProperty()

    def update_device_info(self, name, brand, model, status):
        self.device_name = name
        self.device_brand = brand
        self.device_status = status

    def info_button_pressed(self):
        print(f"Info button pressed for device")