# Popup custom PampaMT

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class PopupPampaMT(Popup):

    text_popup = ObjectProperty(None)
    title = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupPampaMT, self).__init__(**kwargs)

        lay_popup = BoxLayout()
        lay_popup.orientation = 'vertical'
        lb_text_popup = Label()
        lb_text_popup.text = self.text_popup
        lay_popup.add_widget(lb_text_popup)

        self.content = lay_popup
        self.title = self.title





