import logging

from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from app.services.device_service import DeviceService
from app.services.client_service import ClientService
from app.entities.client import Client as ClientEntity
from app.entities.device import Device as DeviceEntity
import app.utils.ui_utils as ui_utilities


class HomeScreen(Screen):

    search_client_popup = None
    search_device_popup = None
    device_info_popup = None
    current_client_id = None

    def on_enter(self, *args):
        self.search_client_popup = SearchClientPopup()
        self.device_info_popup = DeviceInformationPopup()
        self.load_pending_devices()
        self.load_repaired_devices()

    def load_pending_devices(self):
        device_service = DeviceService()
        pending_list = device_service.list_devices_by_status(status="Defective")

        for device in pending_list:
            device_view_model = DeviceStatusItemViewModel.from_entity(device)
            self.ids.pending_container.add_widget(device_view_model)

    def load_repaired_devices(self):
        device_service = DeviceService()
        complete_list = device_service.list_devices_by_status(status="Repaired")

        for device in complete_list:
            device_status_item = DeviceStatusItemViewModel.from_entity(device)
            self.ids.complete_container.add_widget(device_status_item)

    def transfer_device(self, device_status_item_view_model):
        device_service = DeviceService()

        if device_status_item_view_model.device_status == "Defective":
            self.ids.pending_container.remove_widget(device_status_item_view_model)
            self.ids.complete_container.add_widget(device_status_item_view_model)
            device_status_item_view_model.device_status = "Repaired"
            device_service.update_device_status(device_status_item_view_model.device_id, "Repaired")

        else:
            self.ids.complete_container.remove_widget(device_status_item_view_model)
            # TODO: update the device 'delivered_at' status in the database.

    def import_client_information(self, client_item_view_model):
        self.ids.client_first_name.text = client_item_view_model.client_first_name
        self.ids.client_last_name.text = client_item_view_model.client_last_name
        self.ids.client_phone_number.text = client_item_view_model.client_phone_number
        self.ids.client_email.text = client_item_view_model.client_email
        self.dismiss_search_client_popup()

    def register_client(self):
        if not ui_utilities.validate_client_registration(self):
            return

        client_first_name = self.ids.client_first_name.text
        client_last_name = self.ids.client_last_name.text
        client_phone_number = self.ids.client_phone_number.text
        client_email = self.ids.client_email.text

        client = ClientEntity(client_first_name, client_last_name, client_phone_number, client_email)
        client_service = ClientService()

        response = client_service.register_client(client)

        if response.success:
            client = response.data
            self.current_client_id = client.client_id
            self.ids.register_device_button.disabled = False
            logging.info("HomeScreen: Registered client successfully.")
            ui_utilities.show_info_message(self, response.message)

        else:
            logging.exception(f"HomeScreen: Failed to register client: {client}.")
            ui_utilities.show_error_message(self, response.message)

    def register_device(self):
        device_service = DeviceService()
        device = DeviceEntity()

        device.device_type = self.ids.device_type.text
        device.device_brand = self.ids.device_brand.text
        device.device_model = self.ids.device_model.text
        device.fault_type = self.ids.fault_type.text
        device.fault_code = self.ids.fault_code.text
        device.fault_level = self.ids.fault_level.text
        device.client_id = self.current_client_id

        try:
            device = device_service.register_device(device)
            self.add_device_to_pending_list(device)
            logging.info(f"HomeScreen: Registered device successfully.")

        except Exception as e:
            logging.exception(f"HomeScreen: Failed to register device: {device}.\n Exception: {e}")

    def add_device_to_pending_list(self, device):
        device_status_item = DeviceStatusItemViewModel.from_entity(device)
        self.ids.pending_container.add_widget(device_status_item)

    def new_client_entry(self):
        ui_utilities.new_client_entry(self)

    def new_device_entry(self):
        ui_utilities.new_device_entry(self)

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

    def set_fault_type(self, value):
        ui_utilities.set_fault_type(self, value)

    def set_device_brand(self, value):
        ui_utilities.set_device_brand(self, value)

    def validate_name(self, widget):
        ui_utilities.validate_name(self, widget)

    def validate_phone_number(self, widget):
        ui_utilities.validate_phone_number(self, widget)

    def validate_email(self, widget):
        ui_utilities.validate_email(self, widget)

    @staticmethod
    def verify_email(widget):
        ui_utilities.verify_email(widget)


class DeviceStatusItemViewModel(MDBoxLayout):
    device_id = NumericProperty()
    device_brand = StringProperty()
    device_status = StringProperty()
    device_entity = None
    client_entity = None
    device_info_popup = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_info_popup = DeviceInformationPopup()
        self.get_client_entity()

    def get_client_entity(self):
        client_service = ClientService()
        self.client_entity = client_service.get_client(self.device_id)
        print(self.client_entity)

    # Factory method:
    @classmethod
    def from_entity(cls, device_entity: DeviceEntity):
        obj = cls(
            device_id=device_entity.device_id,
            device_brand=device_entity.device_brand,
            device_status=device_entity.device_status,
        )
        obj.device_entity = device_entity
        return obj

    def open_device_info_popup(self):
        self.device_info_popup.client_full_name = "Baki Hanma"
        self.device_info_popup.device_entity = self.device_entity
        self.device_info_popup.client_entity = self.client_entity
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
    client_full_name = StringProperty()
    client_phone_number = StringProperty()
    device_id = StringProperty()
    device_type = StringProperty()
    device_brand = StringProperty()
    device_model = StringProperty()
    fault_code = StringProperty()
    fault_type = StringProperty()
    fault_level = StringProperty()
    device_entity = None
    client_entity = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_open(self):
        print(self.device_entity)
        print(self.client_entity)


class DeviceIemViewModel(MDBoxLayout):
    pass


class SearchClientPopup(Popup):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.client_service = ClientService()
        self.clients_list = list()
        self.search_filter = "First Name"

    def on_open(self):
        self.clients_list = self.client_service.list_clients()
        self.load_client_items(self.clients_list)

    def load_client_items(self, clients_list):
        self.ids.search_client_container.clear_widgets()

        for client in clients_list:
            client_item = ClientItemViewModel(
                client_first_name=client.first_name,
                client_last_name=client.last_name,
                client_phone_number=client.phone_number,
                client_email=client.email,
            )

            self.ids.search_client_container.add_widget(client_item)

    def filter_by(self, search_filter):
        self.search_filter = search_filter

    def search_client(self, search_text):
        if search_text:
            filtered_clients = self.filter_clients(search_text)
            self.load_client_items(filtered_clients)
        else:
            self.load_client_items(self.clients_list)

    def filter_clients(self, search_text):
        if self.search_filter == "First Name":
            return [client for client in self.clients_list if search_text.lower() in client.first_name.lower()]
        elif self.search_filter == "Last Name":
            return [client for client in self.clients_list if search_text.lower() in client.last_name.lower()]
        elif self.search_filter == "Phone Number":
            return [client for client in self.clients_list if search_text in client.phone_number]
        else:
            return self.clients_list
