# Button black

from kivy.uix.button import Button
import os
user = os.environ['HOME']
class ButtonBlack(Button):
    def __init__(self, **kwargs):
        super(ButtonBlack, self).__init__(**kwargs)
        self.background_normal = user + '/.PampaMT/source/kivy_pampamt/fig_kivyppmt/background_button_black.png'
        self.size_hint = None, None
        self.height = 30
        self.width = 130