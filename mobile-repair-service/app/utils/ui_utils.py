import re


def show_error_message(instance, message):
    instance.ids.input_validation.text = f"[color=#ff0000]*[/color][i] {message}[/i]"


def show_info_message(instance, message):
    instance.ids.input_validation.text = f"[color=#00ff00]*[/color][i] {message}[/i]"


def validate_client_registration(instance):
    first_name = instance.ids.client_first_name.text
    last_name = instance.ids.client_last_name.text
    phone_number = instance.ids.client_phone_number.text

    if first_name == '' and last_name == '' and phone_number == '':
        instance.ids.input_validation.text = \
            "[color=#ff0000]*[/color] [i]Please fill in the client's required information.[/i]"
        return False

    else:
        return True


def validate_name(instance, widget):
    if widget.text == "":
        print("client name must not be empty")
        instance.ids.input_validation.text = \
            "[color=#ff0000]*[/color] [i]Client name must not be empty.[/i]"


def validate_email(instance, widget):
    if not widget.focus and widget.text != "":
        if not instance.verify_email(widget):
            instance.ids.input_validation.text = \
                "[color=#ff0000]*[/color] [i]Email format is not correct.[/i]"
    else:
        instance.ids.input_validation.text = ""


def validate_phone_number(instance, widget):
    if widget.text == "":
        instance.ids.input_validation.text = \
            "[color=#ff0000]*[/color] [i]Client phone number must not be empty.[/i]"

    if len(widget.text) != 8:
        return print("invalid phone number!")


def verify_email(widget):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(pattern, widget.text):
        print("correct email!")
        return True
    else:
        print("incorrect email!")
        return False


def set_fault_type(instance, value):
    if value == "Hardware":
        instance.ids.fault_code.values = ["HF01", "HF02", "HF03", "HF04", "HF05"]
    else:
        instance.ids.fault_code.values = ["FF01", "FF02", "FF03", "FF04", "FF05"]


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


def new_client_entry(instance):
    instance.current_client_id = None
    instance.ids.client_first_name.text = ''
    instance.ids.client_last_name.text = ''
    instance.ids.client_phone_number.text = ''
    instance.ids.client_email.text = ''
    instance.ids.register_device.disabled = True


def new_device_entry(instance):
    instance.ids.device_type.text = 'Mobile'
    instance.ids.device_brand.text = ''
    instance.ids.device_model.text = ''
    instance.ids.fault_type.text = ''
    instance.ids.fault_code.text = ''
    instance.ids.fault_level.text = ''
