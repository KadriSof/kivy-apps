import logging
import re

from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from app.services.device_service import DeviceService
from app.services.client_service import ClientService
from app.entities.device import Device as DeviceEntity


class HomeScreen(Screen):

    search_client_popup = None
    search_device_popup = None
    device_info_popup = None

    def on_enter(self, *args):
        self.search_client_popup = SearchClientPopup()
        self.device_info_popup = DeviceInformationPopup()
        self.load_pending_devices()
        self.load_repaired_devices()

    def load_pending_devices(self):
        device_service = DeviceService()
        pending_list = device_service.list_devices_by_status(status="Defective")
        print(pending_list)

        for device in pending_list:
            device_status_item = DeviceStatusItemViewModel(
                device_id=str(device.device_id),
                device_name=f"Device n° {device.device_id}",
                device_brand=device.device_brand,
            )
            self.ids.pending_container.add_widget(device_status_item)

    def load_repaired_devices(self):
        device_service = DeviceService()
        complete_list = device_service.list_devices_by_status(status="Repaired")

        for device in complete_list:
            device_status_item = DeviceStatusItemViewModel(
                device_id=str(device.device_id),
                device_name=f"Device n° {device.device_id}",
                device_brand=device.device_brand,
                device_status=device.device_status,
            )
            self.ids.complete_container.add_widget(device_status_item)

    def open_search_client_popup(self):
        self.search_client_popup.open()

    def open_search_device_popup(self):
        self.search_device_popup.open()

    def open_device_info_popup(self):
        self.device_info_popup.open()

    def dismiss_search_client_popup(self):
        self.search_client_popup.dismiss()

    def dismiss_search_device_popup(self):
        self.search_device_popup.dismiss()

    def dismiss_device_info_popup(self):
        self.device_info_popup.dismiss()

    def transfer_device(self, device_status_item_view_model):
        device_service = DeviceService()

        if device_status_item_view_model.device_status == "Defective":
            self.ids.pending_container.remove_widget(device_status_item_view_model)
            self.ids.complete_container.add_widget(device_status_item_view_model)
            device_status_item_view_model.device_status = "Repaired"
            device_service.update_device_status(device_status_item_view_model.device_id, "Repaired")

        else:
            self.ids.complete_container.remove_widget(device_status_item_view_model)
            # TODO: Add the a call for the "register_device()" method.

    def import_client_information(self, client_item_view_model):
        self.ids.client_first_name.text = client_item_view_model.client_first_name
        self.ids.client_last_name.text = client_item_view_model.client_last_name
        self.ids.client_phone_number.text = client_item_view_model.client_phone_number
        self.ids.client_email.text = client_item_view_model.client_email
        self.dismiss_search_client_popup()

    def register_device(self):
        device_type = self.ids.device_type.text
        device_brand = self.ids.device_brand.text
        device_model = self.ids.device_model.text
        fault_type = self.ids.fault_type.text
        fault_code = self.ids.fault_code.text
        fault_level = self.ids.fault_level.text

        device = DeviceEntity(device_type, device_brand, device_model, fault_type, fault_code, fault_level)
        device_service = DeviceService()

        try:
            device = device_service.register_device(device)
            self.add_device_to_pending_list(device)
            logging.info(f"HomeScreen: Registered device: {device}")

        except Exception as e:
            logging.exception(f"HomeScreen: Failed to register device: {device}")

    def add_device_to_pending_list(self, device):
        device_status_item = DeviceStatusItemViewModel(
            device_name=f"Device n° {device.device_id}",
            device_brand=device.device_brand,
        )
        self.ids.pending_container.add_widget(device_status_item)

    # TODO: Adjust the information entry configuration logic.
    def set_fault_type(self, value):
        if value == "Hardware":
            self.ids.fault_code.values = ["HF01", "HF02", "HF03", "HF04", "HF05"]
        else:
            self.ids.fault_code.values = ["FF01", "FF02", "FF03", "FF04", "FF05"]

    def set_device_brand(self, value):
        if value == "Mobile":
            self.ids.device_brand.values = \
                ['Samsung', 'Huawei', 'Oppo', 'Xiaomi', 'Iphone', 'Nokia', 'Other']

        elif value == "PC":
            self.ids.device_brand.values = \
                ['Asus', 'Apple', 'MSI', 'HP', 'Dell', 'Lenovo', 'Toshiba', 'Samsung', 'Other']

        else:
            self.ids.device_brand.values = \
                ['Apple', 'Google', 'OnePlus', 'Oppo', 'Samsung', 'Vivo', 'Xiaomi', 'Other']

    def validate_name(self, widget):
        if widget.text == "":
            print("client name must not be empty")
            self.ids.input_validation.text = \
                "[color=#ff0000]*[/color] [i]Client name must not be empty.[/i]"

    def validate_email(self, widget):
        if not widget.focus and widget.text != "":
            if not self.verify_email(widget):
                self.ids.input_validation.text = \
                    "[color=#ff0000]*[/color] [i]Email format is not correct.[/i]"
        else:
            self.ids.input_validation.text = ""

    def validate_phone_number(self, widget):
        if widget.text == "":
            self.ids.input_validation.text = \
                "[color=#ff0000]*[/color] [i]Client phone number must not be empty.[/i]"

        if len(widget.text) != 8:
            return print("invalid phone number!")

    @staticmethod
    def verify_email(widget):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if re.match(pattern, widget.text):
            print("correct email!")
            return True
        else:
            print("incorrect email!")
            return False


class DeviceStatusItemViewModel(MDBoxLayout):
    device_id = StringProperty()
    device_name = StringProperty()
    device_brand = StringProperty()
    device_status = StringProperty(defaultvalue="Defective")
    device_info_popup = None

    def __init__(self, device_id, device_name, device_brand, device_status="Defective", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_id = device_id
        self.device_name = device_name
        self.device_brand = device_brand
        self.device_status = device_status
        self.device_info_popup = DeviceInformationPopup()

    def get_device_info(self):
        print(self.device_status)

    def open_device_info_popup(self):
        self.device_info_popup.open()

    def check_button_pressed(self, transfer_callback):
        """Handle the check button press."""
        transfer_callback(self)


class ClientItemViewModel(MDBoxLayout):
    client_first_name = StringProperty()
    client_last_name = StringProperty()
    client_phone_number = StringProperty()
    client_email = StringProperty()

    def __init__(self, client_first_name, client_last_name, client_email, client_phone_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_first_name = client_first_name
        self.client_last_name = client_last_name
        self.client_email = client_email if client_email else ""
        self.client_phone_number = client_phone_number


class DeviceInformationPopup(Popup):
    pass


class DeviceIemViewModel(MDBoxLayout):
    pass


class SearchClientPopup(Popup):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.client_service = None

    def on_open(self):
        client_service = ClientService()
        clients_list = client_service.list_clients()
        self.load_client_items(clients_list)

    def load_client_items(self, clients_list):
        for i in range(len(clients_list)):
            client_item = ClientItemViewModel(
                client_first_name=clients_list[i].first_name,
                client_last_name=clients_list[i].last_name,
                client_email=clients_list[i].email,
                client_phone_number=clients_list[i].phone_number,
            )
            self.ids.search_client_container.add_widget(client_item)
