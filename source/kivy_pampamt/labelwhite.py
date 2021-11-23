from kivy.lang import Builder
from kivy.uix.label import Label

kivy_code_label_white = """
<LabelWhite>:
    canvas.before:
        Color:
            rgba: 1.,1.,1.,.8
        Rectangle:
            size: self.size
            pos: self.pos

"""
Builder.load_string(kivy_code_label_white)
class LabelWhite(Label):
    pass