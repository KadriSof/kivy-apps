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


def show_error_message(instance, message):
    instance.ids.input_validation.text = f"[color=#ff0000]*[/color][i] {message}[/i]"


def show_info_message(instance, message):
    instance.ids.input_validation.text = f"[color=#00ff00]*[/color][i] {message}[/i]"
