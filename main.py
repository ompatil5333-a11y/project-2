import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.widget import Widget
import qrcode

# Set background color
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class QuickPayRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        # App Title
        title = Label(
            text='💸 QuickPay - QR Code Generator',
            size_hint_y=None,
            height=50,
            color=(0.1, 0.4, 0.7, 1),
            font_size='22sp',
            bold=True
        )
        self.add_widget(title)

        # Amount Input
        self.amount_input = TextInput(
            hint_text='Enter Amount (e.g. 250.00)',
            size_hint_y=None,
            height=50,
            input_filter='float',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10],
            font_size='16sp'
        )
        self.add_widget(self.amount_input)

        # UPI Input
        self.upi_input = TextInput(
            hint_text='Enter UPI ID (e.g. name@bank)',
            size_hint_y=None,
            height=50,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10],
            font_size='16sp'
        )
        self.add_widget(self.upi_input)

        # App selection
        self.app_spinner = Spinner(
            text='Select App',
            values=('PhonePe', 'GPay', 'BHIM', 'Paytm', 'Others'),
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        self.add_widget(self.app_spinner)

        # Generate Button
        self.gen_btn = Button(
            text='Generate QR Code',
            size_hint_y=None,
            height=55,
            background_normal='',
            background_color=(0, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.gen_btn.bind(on_release=self.generate_qr)
        self.add_widget(self.gen_btn)

        # QR Image Display
        self.qr_image = Image(
            size_hint=(1, None),
            height=320,
            keep_ratio=True,
            allow_stretch=True
        )
        self.add_widget(self.qr_image)

        # Footer
        self.footer = Label(
            text='© 2025 QuickPay | Developed by Som',
            size_hint_y=None,
            height=30,
            font_size='12sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        self.add_widget(self.footer)

    def show_message(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(.8, .4),
            background_color=(1, 1, 1, 1),
        )
        popup.open()

    def generate_qr(self, *args):
        amount = self.amount_input.text.strip()
        upi = self.upi_input.text.strip()
        app_selected = self.app_spinner.text

        if not amount or not upi or app_selected == 'Select App':
            self.show_message('Error', '⚠ Please fill all fields and select a payment app')
            return

        # Build UPI payload
        data = f"upi://pay?pa={upi}&pn=QuickPay&am={amount}&cu=INR"

        # Save directory
        app = App.get_running_app()
        out_dir = os.path.join(app.user_data_dir, 'output_qr')
        os.makedirs(out_dir, exist_ok=True)

        safe_upi = upi.replace('@', '_at_')
        filename = os.path.join(out_dir, f"{app_selected}_QuickPay_{safe_upi}_{amount}.png")

        # Generate QR
        qr = qrcode.make(data)
        qr.save(filename)

        # Display QR
        self.qr_image.source = filename
        self.qr_image.reload()

        self.show_message('Success', f'✅ QR saved to:\n{filename}')


class QuickPayApp(App):
    def build(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        return QuickPayRoot()


if __name__ == '__main__':
    QuickPayApp().run()

