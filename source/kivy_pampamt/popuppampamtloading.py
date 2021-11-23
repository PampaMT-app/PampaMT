# Popup Custom PampaMT Loading

from kivy.uix.label import Label
from source.kivy_pampamt.buttonpampamt import ButtonBlack
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar


from kivy.properties import ObjectProperty

import threading



class PopUpLoading(Popup):

    cancel = ObjectProperty(None)
    title_pop = ObjectProperty(None)
    num_max = ObjectProperty(None)

    lang_seconds = ObjectProperty(None)
    lang_minutes = ObjectProperty(None)
    lang_cancel = ObjectProperty(None)

    count_time = 0
    time_one_step = 0

    def __init__(self, **kwargs):
        super(PopUpLoading, self).__init__(**kwargs)

        box_lay_popup = BoxLayout()
        box_lay_popup.orientation = 'vertical'

        self.bt_ok = ButtonBlack(text=self.lang_cancel)
        self.bt_ok.opacity = 1.
        self.bt_ok.on_press = self.cancel
        self.lb_status = Label()
        self.lb_status.text = '0 %'

        self.progre_bar = ProgressBar()

        box_bar = BoxLayout()
        box_bar.add_widget(Label(size_hint_x=None, width=5))
        box_bar.add_widget(self.progre_bar)
        box_bar.add_widget(Label(size_hint_x=None, width=5))


        box_bt = BoxLayout()
        box_bt.add_widget(Label())
        box_bt.add_widget(self.bt_ok)
        box_bt.add_widget(Label())

        box_lay_popup.add_widget(box_bar)
        box_lay_popup.add_widget(self.lb_status)
        box_lay_popup.add_widget(box_bt)
        self.content = box_lay_popup
        self.title = self.title_pop
        self.title_size = 16
        self.size_hint = None, None
        self.height = 150
        self.width = 300
        self.auto_dismiss = False


        parallel_progress_bar = threading.Thread(target=Clock.schedule_once, args=(self.press_ok,))
        parallel_progress_bar.start()

    def press_ok(self, instance):
        self.progre_bar.value = 1
        Clock.schedule_interval(self.next, .0005)

    def next(self, dt):

        if self.progre_bar.value >= 100:
            return False

        check_time = 0
        if self.count_time != check_time:

            value_step = ((self.count_time*100)/self.num_max)
            self.progre_bar.value = int(value_step)
            time_left = (self.num_max - self.count_time) * self.time_one_step

            if time_left > 60:
                self.lb_status.text = str(self.progre_bar.value) + ' %                         ' + \
                                      str(round(time_left/60)) + ' ' + self.lang_minutes
            else:
                self.lb_status.text = str(self.progre_bar.value) + ' %                         ' + \
                                      str(round(time_left)) + ' ' + self.lang_seconds
            check_time = self.count_time


    def papallel_start(self,funtion):
        parallel_function = threading.Thread(target=funtion)
        parallel_function.start()


"""
#    EXEMPLO:
    
from timeit import default_timer as timer
import time


class Tela(BoxLayout):
    def __init__(self, **kwargs):
        super(Tela, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.pop = PopUpLoading(title_pop='Copying...', lang_seconds='segundos', lang_minutes='minutos', lang_cancel='cancel')

        #elf.add_widget(self.pop)

        bt = ButtonBlack(text='OK')
        bt.on_press = self.openpop
        self.add_widget(bt)

    def openpop(self):
        self.pop.open()
        self.pop.num_max = 100
        self.pop.papallel_start(self.sleep)



    def sleep(self):
        for i in range(101):
            time1 = timer()

            time.sleep(.05)
            print('sleep' + str(i))
            self.pop.count_time = i
            time2 = timer()
            self.pop.time_one_step = time2 - time1
            i += 1


from kivy.app import App

class janela(App):
    def build(self):
        return Tela()

janela().run()
"""