from datetime import datetime

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from app.database.session import get_session
from app.repositories.device_repository import DeviceRepository
from app.services.device_service import DeviceService


class HomeScreen(Screen):

    def on_enter(self, *args):
        for i in range(5):
            device = DeviceItemViewModel(
                device_name="Device n° {i}".format(i=i),
                device_brand="IPhone",
            )
            self.ids.pending_container.add_widget(device)

    def transfer_device(self, device_item_view_model):
        if device_item_view_model.device_status == "Defective":
            self.ids.pending_container.remove_widget(device_item_view_model)
            self.ids.complete_container.add_widget(device_item_view_model)
            device_item_view_model.device_status = "Repaired"

        else:
            self.ids.complete_container.remove_widget(device_item_view_model)
            # TODO: Add the a call for the "register_device()" method.

    def register_device(self):
        device_type = self.ids.device_type.text
        device_brand = self.ids.device_brand.text
        device_model = self.ids.device_model.text
        fault_type = self.ids.fault_type.text
        fault_level = self.ids.fault_level.text
        print(f"Device Type: {device_type}\n"
              f"Device Brand: {device_brand}\n"
              f"Device Model: {device_model}\n"
              f"Fault Type: {fault_type}\n"
              f"Fault Level: {fault_level}\n")

        # TODO: Figure out how to change the session handling to the service layer.
        # session = get_session()
        # try:
        #     # Pass the session to the repository
        #     device_repository = DeviceRepository(session)
        #     device_service = DeviceService(device_repository)
        #     device = device_service.create_device(device_type, device_brand, device_model, device_status)
        #     device_service.register_device(device)
        #
        #     # Commit the session if everything is successful
        #     session.commit()
        # except Exception as e:
        #     # Rollback the session in case of any errors
        #     session.rollback()
        #     print(f"Error occurred: {e}")
        # finally:
        #     # Close the session
        #     session.close()

    # TODO: Adjust the information entry configuration logic.
    def configure_device_information_entry(self, value):
        if value == "Hardware":
            self.ids.fault_code.values = ["HF01", "HF02", "HF03", "HF04", "HF05"]
        else:
            self.ids.fault_code.values = ["FF01", "FF02", "FF03", "FF04", "FF05"]


class DeviceItemViewModel(MDBoxLayout):
    device_name = StringProperty()
    device_brand = StringProperty()
    device_status = StringProperty(defaultvalue="Defective")

    def __init__(self, device_name, device_brand, device_status="Defective", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_name = device_name
        self.device_brand = device_brand
        self.device_status = device_status

    def get_device_info(self):
        print(self.device_status)

    def check_button_pressed(self, transfer_callback):
        """Handle the check button press."""
        transfer_callback(self)
