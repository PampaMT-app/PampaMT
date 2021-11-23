from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.accordion import AccordionItem
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton


from kivy.properties import ObjectProperty

from kivy.graphics import Color, Rectangle

import os
import glob
import threading
import time
from timeit import default_timer as timer


from kivy.lang import Builder

from source.site import FileAsc
from source.kivy_pampamt.buttonpampamt import ButtonBlack
from source.kivy_pampamt.labelwhite import LabelWhite
from source.kivy_pampamt.popuppampamtloading import PopUpLoading
from source.tools.convert_exp_to_si import NumberSI
from source.project import save
user = os.environ['HOME']

code_kivy_processingZ = """
#: import o os
<ProcessingZ>:
    orientation: 'horizontal'
    BoxLayout: 
        size_hint_x: None
        width: 200
        id: box_sites
        orientation: 'vertical'
        
        canvas.before:
            Color:
                rgba: 1.,1.,1.,.1
            Rectangle:
                size: self.size
                pos: self.pos
        
        Label:
            text: 'Sites'
            size_hint_y: None
            height: 30
            canvas.before:
                Color:
                    rgba: 0,0,0,.5
                Rectangle:
                    size: self.size
                    pos: self.pos
        Label:
            size_hint_y: None
            height: 1
            canvas.before:
                Color:
                    rgba: 1.,1.,1.,.8
                Rectangle:
                    size: self.size
                    pos: self.pos        
        ScrollView:
            size_hint_x: None
            width: 200
            Accordion
                height: root.size_accordeon_scroll
                id: accor_sites
                orientation: 'vertical'
                size_hint_y: None
                min_space: 25
    
    Label:
        size_hint_x: None
        width: 2
        canvas.before:
            Color:
                rgba: 1.,1.,1.,.01
            Rectangle:
                size: self.size
                pos: self.pos
    
    Label:
        size_hint_x: None
        width: 1
        canvas.before:
            Color:
                rgba: 1.,1.,1.,.8
            Rectangle:
                size: self.size
                pos: self.pos 
    Label:
        size_hint_x: None
        width: 1
        canvas.before:
            Color:
                rgba: 1.,1.,1.,.01
            Rectangle:
                size: self.size
                pos: self.pos
    Label:
        size_hint_x: None
        width: 1
        canvas.before:
            Color:
                rgba: 1.,1.,1.,.8
            Rectangle:
                size: self.size
                pos: self.pos           
          
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            TabbedPanel:
                do_default_tab: False
                tab_height: 25
                tab_width: 150
                id: tab_asc
                
                
                
        Label:
            size_hint_y: None
            height: 1
            canvas.before:
                Color:
                    rgba: 1.,1.,1.,.8
                Rectangle:
                    size: self.size
                    pos: self.pos  
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1.,1.,1.,.1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    
            size_hint_y: None
            height: 100
            
            BoxLayout:
                orientation: 'vertical'
                
                Label:
                BoxLayout:
                    Label:
                        size_hint_x: None
                        width: 10
                    ButtonBlack:
                        id: bt_cancel
                    Label:
                    ButtonBlack:
                        width: 150
                        id: bt_processingZ 
                        on_press: root.open_popup_processingZ()
                    Label:
                        size_hint_x: None
                        width: 10
                Label:
            
    
<ViewButton@ButtonBehavior+Label>:
    size_hint_y: None
    height: 25
    color: 1,1,1,1
    
<LabelDiv@Label>:
    size_hint_y: None
    height: 1
    canvas.before:
        Color:
            rgba: 1.,1.,1.,.5
        Rectangle:
            size: self.size
            pos: self.pos


<ViewFilesAscADU06>:
    orientation: 'vertical'
    LabelDiv:
    ViewButton:
        text: root.band + '                               A'
        id: band_A
        on_press: root.print_back(self)
        band: 'A'
    LabelDiv:
    
    ViewButton:
        text: root.band + '                               B'
        id: band_B
        on_press: root.print_back(self)
        band: 'B'
    LabelDiv:
    
    ViewButton:
        text: root.band + '                               F'
        id: band_F
        on_press: root.print_back(self)
        band: 'F'
    LabelDiv:
    
    ViewButton:
        text: root.band + '                               C'
        id: band_C
        on_press: root.print_back(self)
        band: 'C'
    LabelDiv:
    
    ViewButton:    
        text: root.band + '                               D'
        id: band_D
        on_press: root.print_back(self)
        band: 'D'
    LabelDiv:
    Label:
    
<ViewFilesAscADU07>:
    orientation: 'vertical'
    LabelDiv:
    ViewButton:
        text: root.band + '                     65536H'
        id: band_65536H
        on_press: root.print_back(self)
        band: '65536H'
    LabelDiv:
    
    ViewButton:
        text: root.band + '                       4096H'
        id: band_4096H
        on_press: root.print_back(self)
        band: '4096H'
    LabelDiv:
    
    ViewButton:
        text: root.band + '                         128H'
        id: band_128H
        on_press: root.print_back(self)
        band: '128H'
    LabelDiv:
    ViewButton:    
        text: root.band + '                             4H'
        id: band_4H
        on_press: root.print_back(self)
        band: '4H'
    LabelDiv:
    Label:

"""

Builder.load_string(code_kivy_processingZ)

list_file_asc = []

class ViewFilesAscADU06(BoxLayout):

    band = ObjectProperty(None)
    get_band = ObjectProperty(None)
    site = ''
    equipment = ' '

    def print_back(self, instancia):

        self.ids.band_A.canvas.before.clear()
        self.ids.band_B.canvas.before.clear()
        self.ids.band_F.canvas.before.clear()
        self.ids.band_C.canvas.before.clear()
        self.ids.band_D.canvas.before.clear()

        instancia.canvas.before.add(Color(rgba=(1., 1., 1., .2)))
        instancia.canvas.before.add(Rectangle(size=instancia.size, pos=instancia.pos))

        self.get_band(instancia.band, self.site, self.equipment)

    def clear_band(self):
        self.ids.band_A.canvas.before.clear()
        self.ids.band_B.canvas.before.clear()
        self.ids.band_F.canvas.before.clear()
        self.ids.band_C.canvas.before.clear()
        self.ids.band_D.canvas.before.clear()

class ViewFilesAscADU07(BoxLayout):

    band = ObjectProperty(None)
    get_band = ObjectProperty(None)
    site = ' '
    equipment = ' '

    def print_back(self, instancia):

        self.ids.band_65536H.canvas.before.clear()
        self.ids.band_4096H.canvas.before.clear()
        self.ids.band_128H.canvas.before.clear()
        self.ids.band_4H.canvas.before.clear()

        instancia.canvas.before.add(Color(rgba=(1., 1., 1., .2)))
        instancia.canvas.before.add(Rectangle(size=instancia.size, pos=instancia.pos))

        print(instancia.text)
        self.get_band(instancia.band, self.site, self.equipment)

    def clear_band(self):
        self.ids.band_65536H.canvas.before.clear()
        self.ids.band_4096H.canvas.before.clear()
        self.ids.band_128H.canvas.before.clear()
        self.ids.band_4H.canvas.before.clear()

class TabItemFilesAsc(TabbedPanelItem):


    file_asc = ObjectProperty(None)
    lang = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(TabItemFilesAsc, self).__init__(**kwargs)
        self.text = self.file_asc.name
        self.textbt = self.file_asc.name

        self.list_ti_frequency = []
        self.list_ti_mode = []

        self.lay_file_asc = BoxLayout()
        self.lay_file_asc.orientation = 'vertical'


        # ====================== Button Add Line in processingZ ====================
        #  Layout to button add line in processing Z
        box_lay_set_button_add_ss = BoxLayout(size_hint_y=None, height=25)
        box_lay_set_button_add_ss.height = 25
        box_lay_set_button_add_ss.add_widget(Label(size_hint_x=None, width=30))

        # Button for add line in file processingZ
        self.bt_add_ss = ButtonBlack(  size_hint_x=None)
        self.bt_add_ss.height = 25
        self.bt_add_ss.width = 25
        self.bt_add_ss.text = '+'
        self.bt_add_ss.on_press = self.add_new_lay_setting_processingZ


        box_lay_set_button_add_ss.add_widget(self.bt_add_ss)
        box_lay_set_button_add_ss.add_widget(Label())
        # ==========================================================================

        self.box_lay_lines_processingZ = BoxLayout()
        self.box_lay_lines_processingZ.orientation = 'vertical'


        # ================================= BoxLayout content file processingZ ======
        # Read file processingZ
        dict_lines = self.read_file_processingZ(self.file_asc)

        # Add line in layout
        for lay in range(self.num_line_file_processingZ):
            self.add_lay_setting_processingZ(dict_lines[str(lay)])
        # ===========================================================================

        # ================================= BoxLayout content clock =================

        self.box_lay_clock = BoxLayout()
        self.box_lay_clock.orientation = 'vertical'


        #            ======= Name File clk
        box_lay_clock_name_clk = BoxLayout()
        box_lay_clock_name_clk.size_hint_y = None
        box_lay_clock_name_clk.height = 30
        box_lay_clock_name_clk.add_widget(Label())
        box_lay_clock_name_clk.add_widget(Label(text=self.nameasc_to_nameclk()))
        box_lay_clock_name_clk.add_widget(Label(size_hint_x=None, width=10))

        self.box_lay_clock.add_widget(box_lay_clock_name_clk)
        self.box_lay_clock.add_widget(self.make_show_clk())
        # ==========================================================================

        # ============= BoxLayout Button Save ======================================

        box_lay_set_button_save = BoxLayout()
        box_lay_set_button_save.size_hint_y = None
        box_lay_set_button_save.height = 30
        box_lay_set_button_save.add_widget(Label())

        bt_save = ButtonBlack()
        bt_save.text = self.lang['Save']
        bt_save.on_press = self.save_change

        box_lay_set_button_save.add_widget(Label())
        box_lay_set_button_save.add_widget(bt_save)
        box_lay_set_button_save.add_widget(Label(size_hint_x=None, width=10))




        # Layout setting file asc
        self.lay_file_asc.add_widget(Label(size_hint_y=None, height=10))
        self.lay_file_asc.add_widget(box_lay_set_button_add_ss)
        self.lay_file_asc.add_widget(Label(size_hint_y=None, height=5))
        self.lay_file_asc.add_widget(self.box_lay_lines_processingZ)
        self.lay_file_asc.add_widget(Label())
        self.lay_file_asc.add_widget(self.box_lay_clock)
        self.lay_file_asc.add_widget(Label())
        self.lay_file_asc.add_widget(box_lay_set_button_save)
        self.lay_file_asc.add_widget(Label(size_hint_y=None, height=5))



        self.content = self.lay_file_asc

        self.read_file_clk()

    def close_bubble_not_set(self, bubble):

        time.sleep(1)
        self.lay_file_asc.remove_widget(bubble)

    def open_bubble_not_set(self, ti_not_set):

        float_lay = FloatLayout()
        float_lay.size_hint = None, None
        float_lay.width = 0
        float_lay.height = 0


        bubble_not_set = Bubble()
        bubble_not_set.size_hint = None, None
        bubble_not_set.width = 80
        bubble_not_set.height = 30
        bubble_not_set.center_x = ti_not_set.center_x
        bubble_not_set.center_y = ti_not_set.center_y - 30
        bubble_not_set.arrow_pos = 'top_mid'
        bubble_not_set.background_color = (1, 0, 0, 1)


        bt_not_set = BubbleButton()
        bt_not_set.font_size = 12

        bt_not_set.text = self.lang['Not_Set']

        bubble_not_set.add_widget(bt_not_set)

        float_lay.add_widget(bubble_not_set)

        #self.add_widget(bubble_not_set)
        self.lay_file_asc.add_widget(float_lay)
        parallel_close = threading.Thread(target=self.close_bubble_not_set, args=(float_lay,))
        parallel_close.start()



    def save_change(self):

        arq_file_asc = open('PampaMT/band_asc/' + self.file_asc.site + '/band_' + self.file_asc.band + '/' + self.file_asc.name , 'w')
        #print('PampaMT/band_asc/' + self.file_asc.site + '/band_' + self.file_asc.band + '/' + self.file_asc.name)

        i = 0
        for number_modes in self.list_ti_frequency:

            if self.list_ti_frequency[i].text == '':
                self.open_bubble_not_set(self.list_ti_frequency[i])

            elif self.list_ti_mode[i].text == '':
                self.open_bubble_not_set(self.list_ti_mode[i])

            else:
                line_save_file_band = self.file_asc.name + ' ' + self.list_ti_frequency[i].text + ' ' + self.list_ti_mode[i].text
                #print(self.file_asc.)
                arq_file_asc.write(line_save_file_band + '\n')
                print(line_save_file_band)
            i += 1

        arq_file_asc.close()



        print('save ')


    def make_show_clk(self):

        box_clk_modes = BoxLayout()
        box_clk_modes.size_hint_y = None
        box_clk_modes.height = 85



        box_mode = BoxLayout()
        box_mode.size_hint_x = None
        box_mode.width = 180
        box_mode.orientation = 'vertical'
        bt_remote_reference = ButtonBlack(text=self.lang['Remote_Reference'])
        bt_remote_reference.on_press = self.not_yet_implemented
        bt_remote_reference.width = 150
        lay_setting_bt_remote_reference = BoxLayout()
        lay_setting_bt_remote_reference.add_widget(Label(size_hint_x=None, width=10))
        lay_setting_bt_remote_reference.add_widget(bt_remote_reference)


        box_mode.add_widget(lay_setting_bt_remote_reference)


        box_clk_modes.add_widget(box_mode)
        box_clk_modes.add_widget(self.clock())
        box_clk_modes.add_widget(Label(size_hint_x=None, width=10))


        return box_clk_modes

    def not_yet_implemented(self):
        popup = Popup(size_hint=[None, None])
        popup.height = 70
        popup.width = 200

        popup.title = self.lang['Not_yet_implemented']
        popup.open()

    def clock(self):

        box_lay = BoxLayout()
        box_lay.orientation = 'vertical'

        sampling_rate, clock_reset, clock_zero = self.read_file_clk()

        lay_sampling_rate = self.lay_sampling_rate(sampling_rate)
        lay_clock_reset = self.lay_clock(clock_reset, self.list_ti_clock_reset, self.lang['Reset'])
        lay_clock_zero = self.lay_clock(clock_zero, self.list_ti_clock_zero, self.lang['Zero'])

        box_lay.add_widget(LabelWhite(size_hint_y=None, height=1))
        box_lay.add_widget(lay_sampling_rate)
        box_lay.add_widget(LabelWhite(size_hint_y=None, height=1))
        box_lay.add_widget(lay_clock_reset)
        box_lay.add_widget(lay_clock_zero)
        box_lay.add_widget(LabelWhite(size_hint_y=None, height=1))


        return box_lay

    def lay_sampling_rate(self, sampling_rate):

        box_lay = BoxLayout()

        box_lay.add_widget(Label(text=self.lang['Sampling_Rate']))

        rate_s = sampling_rate[0]

        rate_Hz = 1/float(rate_s)

        text_lb_rate_s = NumberSI()
        text_lb_rate_s.read_number(rate_s)
        text_lb_rate_s.unit = 's'
        text_convert_lb_rate_s = text_lb_rate_s.scientific_notation_to_SI()


        lb_rate_s = Label(text=text_convert_lb_rate_s)



        lb_rate_Hz = Label(text=(str(round(rate_Hz,2))+' Hz'))




        box_lay.add_widget(lb_rate_s)
        box_lay.add_widget(lb_rate_Hz)

        print(rate_s)


        return box_lay





    list_ti_clock_reset = []
    list_ti_clock_zero = []
    def lay_clock(self, clock, list_ti, type_clock):

        ti_yr = TextInput(multiline=False, font_size=12)
        ti_yr.text = clock[0]
        list_ti.append(ti_yr)


        ti_mo = TextInput(multiline=False, font_size=12)
        ti_mo.text = clock[1]
        list_ti.append(ti_mo)

        ti_day = TextInput(multiline=False, font_size=12)
        ti_day.text = clock[2]
        list_ti.append(ti_day)


        ti_hr = TextInput(multiline=False, font_size=12)
        ti_hr.text = clock[3]
        list_ti.append(ti_hr)


        ti_min = TextInput(multiline=False, font_size=12)
        ti_min.text = clock[4]
        list_ti.append(ti_min)

        ti_sec = TextInput(multiline=False, font_size=12)
        ti_sec.text = clock[5]
        list_ti.append(ti_sec)

        ele_time = self.lang['Elements_Time']
        ele_time = ele_time.split(',')

        lb_yr = Label(font_size = 12)
        lb_yr.text = ele_time[0]

        lb_mo = Label(font_size=12)
        lb_mo.text = ele_time[1]

        lb_day = Label(font_size=12)
        lb_day.text = ele_time[2]

        lb_hr = Label(font_size=12)
        lb_hr.text = ele_time[3]

        lb_min = Label(font_size=12)
        lb_min.text = ele_time[4]

        lb_sec = Label(font_size=12)
        lb_sec.text = ele_time[5]



        box_lay = BoxLayout()

        lb_type_clock = Label(font_size=12, text=type_clock)

        box_lay.add_widget(lb_type_clock)
        box_lay.add_widget(lb_yr)
        box_lay.add_widget(ti_yr)

        box_lay.add_widget(lb_mo)
        box_lay.add_widget(ti_mo)

        box_lay.add_widget(lb_day)
        box_lay.add_widget(ti_day)

        box_lay.add_widget(lb_hr)
        box_lay.add_widget(ti_hr)

        box_lay.add_widget(lb_min)
        box_lay.add_widget(ti_min)

        box_lay.add_widget(lb_sec)
        box_lay.add_widget(ti_sec)

        return box_lay

    def read_file_clk(self):

        nameclk = self.nameasc_to_nameclk()
        arq_clk = open('DATA/' + nameclk, 'r')

        i = 0
        for line in arq_clk:
            if i == 0:
                sampling_rate = line

            elif i == 1:
                clock_reset = line

            else:
                clock_zero = line

            i += 1

        sampling_rate = sampling_rate.split()
        clock_reset = clock_reset.split()
        clock_zero = clock_zero.split()

        print('')
        print('Clock: ')
        print(sampling_rate)
        print(clock_reset)
        print(clock_zero)

        text_clk = arq_clk.read()
        arq_clk.close()

        return sampling_rate, clock_reset, clock_zero






    def nameasc_to_nameclk(self):

        nameasc = self.file_asc.name
        nameclk = nameasc.replace(".asc", ".clk")

        return nameclk

    def add_new_lay_setting_processingZ(self):

        line_file_asc = [self.file_asc.name, '', '']
        self.num_line_file_processingZ += 1

        self.line_processingZ = self.make_lay_setting_processingZ(line_file_asc)
        self.box_lay_lines_processingZ.add_widget(self.line_processingZ)


    def add_lay_setting_processingZ(self, line_file_asc):

        self.line_processingZ = self.make_lay_setting_processingZ(line_file_asc)
        self.box_lay_lines_processingZ.add_widget(self.line_processingZ)



    def make_lay_setting_processingZ(self, line_file_asc):

        box_setting_processingZ = BoxLayout()
        box_setting_processingZ.size_hint_y = None
        box_setting_processingZ.height = 30

        box_setting_processingZ.add_widget(Label(text=line_file_asc[0]))

        ti_frequency = TextInput(text=line_file_asc[1])
        ti_frequency.multiline = False
        ti_frequency.size_hint_x = None
        ti_frequency.width = 200
        self.list_ti_frequency.append(ti_frequency)


        ti_mode = TextInput(text=line_file_asc[2])
        ti_mode.multiline = False
        ti_mode.size_hint_x = None
        ti_mode.width = 80
        self.list_ti_mode.append(ti_mode)


        box_setting_processingZ.add_widget(ti_frequency)
        box_setting_processingZ.add_widget(ti_mode)
        box_setting_processingZ.add_widget(Label(size_hint_x=None, width=10))

        return box_setting_processingZ



    num_line_file_processingZ = 0
    def read_file_processingZ(self, file_asc):


        dict_file_processingZ = {}

        print('PampaMT/band_asc/' + file_asc.site + '/band_' + file_asc.band + '/' + file_asc.name)

        arq_file_processingZ = open('PampaMT/band_asc/' + file_asc.site + '/band_' + file_asc.band + '/' + file_asc.name, 'r')


        for line_all in arq_file_processingZ:

            line = line_all.split()

            dict_file_processingZ[str(self.num_line_file_processingZ)] = line

            self.num_line_file_processingZ += 1

        arq_file_processingZ.close()

        return dict_file_processingZ




class ProcessingZ(BoxLayout):


    size_accordeon_scroll = ObjectProperty(None)
    lang = ObjectProperty(None)
    openPampaMT = ObjectProperty(None)


    def __init__(self, list_site, project, **kwargs):

        super(ProcessingZ, self).__init__(**kwargs)

        self.ids.bt_processingZ.text = self.lang['ProcessingZ']
        self.ids.bt_cancel.text = self.lang['Cancel']

        self.list_sites = list_site

        self.project = project

        for site in list_site:

            self.site_acordion = AccordionItem()


            self.site_acordion.title = site.name
            self.site_acordion.min_space = 25

            self.make_file_band_asc(site)

            if site.equipment == 'ADU06':
                view_files_asc06 = ViewFilesAscADU06(band=self.lang['Band'], get_band=self.change_tabs)
                view_files_asc06.site = site.name
                view_files_asc06.equipment = site.equipment
                self.site_acordion.add_widget(view_files_asc06)

            elif site.equipment == 'ADU07':

                view_files_asc07 = ViewFilesAscADU07(band=self.lang['Band'], get_band=self.change_tabs)
                view_files_asc07.site = site.name
                view_files_asc07.equipment = site.equipment
                self.site_acordion.add_widget(view_files_asc07)

            self.ids.accor_sites.add_widget(self.site_acordion)



    # d = TabbedPanel()
    # d.clear_tabs()
    # d.cl
    def change_tabs(self, band, site, equipment):

        self.ids.tab_asc.clear_tabs()
        self.ids.tab_asc.clear_widgets()

        for file_asc in list_file_asc:
            if (file_asc.site == site) and (file_asc.equipment == equipment) and (file_asc.band == band):

                tab_file_asc = TabItemFilesAsc(file_asc=file_asc, lang=self.lang)


                if equipment == 'ADU07':
                    self.ids.tab_asc.tab_width = 230

                self.ids.tab_asc.add_widget(tab_file_asc)

        print('Select Band: ' + band)
        print('Select Site: ' + site)
        print('Select Equipment: ' + equipment)
        print('')

    def make_file_band_asc(self, site):

        if site.equipment == 'ADU06':
            path_band_asc_site = user + '/PampaMT/PROC_MT/' + site.project + '/PampaMT/band_asc/' + site.name
            if os.path.isdir(path_band_asc_site):
                pass
            else:
                os.mkdir(path_band_asc_site)

            # Band A
            print('Band A')
            path_band_asc_site_bandA = path_band_asc_site + '/band_A'

            if os.path.isdir(path_band_asc_site_bandA):
                pass
            else:
                os.mkdir(path_band_asc_site_bandA)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*A.asc')
            path_file_asc = sorted(path_file_asc)

            for path_asc in path_file_asc:

                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = 'A'

                list_file_asc.append(object_file_asc)



                arq_asc = open(path_band_asc_site_bandA + '/' + file_asc, 'w')
                arq_asc.write(file_asc + ' 65536 ss;bs1\n')
                arq_asc.close()

                print(file_asc)

            # Band B
            print('Band B')
            path_band_asc_site_bandB = path_band_asc_site + '/band_B'

            if os.path.isdir(path_band_asc_site_bandB):
                pass
            else:
                os.mkdir(path_band_asc_site_bandB)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*B.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = 'B'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_bandB + '/' + file_asc, 'w')
                arq_asc.write(file_asc + ' 65536 ss\n')
                arq_asc.write(file_asc + '  8192 ss\n')
                arq_asc.close()

                print(file_asc)

            # Band F
            print('Band F')
            path_band_asc_site_bandF = path_band_asc_site + '/band_F'

            if os.path.isdir(path_band_asc_site_bandF):
                pass
            else:
                os.mkdir(path_band_asc_site_bandF)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*F.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = 'F'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_bandF + '/' + file_asc, 'w')
                arq_asc.write(file_asc + ' 16384 ss\n')
                arq_asc.write(file_asc + '  8192 ss\n')
                arq_asc.close()

                print(file_asc)

            # Band C
            print('Band C')
            path_band_asc_site_bandC = path_band_asc_site + '/band_C'

            if os.path.isdir(path_band_asc_site_bandC):
                pass
            else:
                os.mkdir(path_band_asc_site_bandC)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*C.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = 'C'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_bandC + '/' + file_asc, 'w')
                arq_asc.write(file_asc + '   256 ss\n')
                arq_asc.write(file_asc + '   128 ss\n')
                arq_asc.close()

                print(file_asc)

            # Band D
            print('Band D')
            path_band_asc_site_bandD = path_band_asc_site + '/band_D'

            if os.path.isdir(path_band_asc_site_bandD):
                pass
            else:
                os.mkdir(path_band_asc_site_bandD)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*D.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = 'D'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_bandD + '/' + file_asc, 'w')
                arq_asc.write(file_asc + '   128 ss\n')
                arq_asc.write(file_asc + '    64 ss\n')
                arq_asc.close()

                print(file_asc)

        if site.equipment == 'ADU07':
            path_band_asc_site = user + '/PampaMT/PROC_MT/' + site.project + '/PampaMT/band_asc/' + site.name
            if os.path.isdir(path_band_asc_site):
                pass
            else:
                os.mkdir(path_band_asc_site)

            # Band 65536H
            print('Band 65536H')
            path_band_asc_site_band65536H = path_band_asc_site + '/band_65536H'

            if os.path.isdir(path_band_asc_site_band65536H):
                pass
            else:
                os.mkdir(path_band_asc_site_band65536H)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*65536H.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = '65536H'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_band65536H + '/' + file_asc, 'w')
                arq_asc.write(file_asc + ' 65536 ss;bs1\n')
                arq_asc.write(file_asc + ' 32768 ss\n')
                arq_asc.close()

                print(file_asc)

            # Band 4096H
            print('Band 4096H')
            path_band_asc_site_band4096H = path_band_asc_site + '/band_4096H'

            if os.path.isdir(path_band_asc_site_band4096H):
                pass
            else:
                os.mkdir(path_band_asc_site_band4096H)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*4096H.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = '4096H'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_band4096H + '/' + file_asc, 'w')
                arq_asc.write(file_asc + ' 65536 ss\n')
                arq_asc.write(file_asc + '  8192 ss\n')
                arq_asc.close()

                print(file_asc)

            # Band 128H
            print('Band 128H')
            path_band_asc_site_band128H = path_band_asc_site + '/band_128H'

            if os.path.isdir(path_band_asc_site_band128H):
                pass
            else:
                os.mkdir(path_band_asc_site_band128H)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*128H.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = '128H'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_band128H + '/' + file_asc, 'w')
                arq_asc.write(file_asc + '   256 ss\n')
                arq_asc.write(file_asc + '   128 ss\n')
                arq_asc.close()

                print(file_asc)

            # Band 4H
            print('Band 4H')
            path_band_asc_site_band4H = path_band_asc_site + '/band_4H'

            if os.path.isdir(path_band_asc_site_band4H):
                pass
            else:
                os.mkdir(path_band_asc_site_band4H)

            path_file_asc = glob.glob(user + '/PampaMT/PROC_MT/' + site.project + '/DATA/' + site.name + '*4H.asc')
            path_file_asc = sorted(path_file_asc)
            for path_asc in path_file_asc:
                file_asc = os.path.basename(path_asc)

                object_file_asc = FileAsc()
                object_file_asc.name = file_asc
                object_file_asc.site = site.name
                object_file_asc.equipment = site.equipment
                object_file_asc.project = site.project
                object_file_asc.band = '4H'

                list_file_asc.append(object_file_asc)

                arq_asc = open(path_band_asc_site_band4H + '/' + file_asc, 'w')
                arq_asc.write(file_asc + '   128 ss\n')
                arq_asc.write(file_asc + '    64 ss\n')
                arq_asc.close()

                print(file_asc)

        site.files_asc = list_file_asc


    def cancel_processingZ(self):
        self.break_processingZ = True

    def open_popup_processingZ(self):

        self.pop_processingZ = PopUpLoading(title_pop='ProcessingZ...', lang_seconds='segundos', lang_minutes='minutos',
                                            lang_cancel='cancel', cancel=self.cancel_processingZ)

        self.pop_processingZ.width = 350

        num_file = len(list_file_asc)

        self.pop_processingZ.open()



        self.pop_processingZ.num_max = num_file
        self.pop_processingZ.papallel_start(self.processingZ)


    def processingZ(self):

        self.break_processingZ = False
        number_file = 1



        for file_asc in list_file_asc:
            time_go = timer()

            if self.break_processingZ == False and file_asc.processingZ == False:

                processingZ = 'PampaMT/band_asc/' + file_asc.site + '/band_' + file_asc.band + '/' + file_asc.name
                time.sleep(1)
                os.system('processamentoZ ' + processingZ)
                file_asc.processingZ = True


                # Save in ppmt file
                self.project.sites = self.list_sites
                #self.project.save()
                save(self.project)

                print(processingZ)
            else:
                print('cancelando..')

                self.pop_processingZ.dismiss()
                break

            self.pop_processingZ.count_time = number_file
            time_end = timer()
            self.pop_processingZ.time_one_step = time_end - time_go
            number_file += 1
            self.pop_processingZ.title = self.pop_processingZ.title_pop + '      ' + file_asc.name

        if self.break_processingZ == False:
            self.pop_processingZ.dismiss()
            self.open_PampaMT()

    def open_PampaMT(self):

        print('salvar, gerar os arquivo para plotar , e abrir o pampa mt')
        # print(self.list_sites)

        self.openPampaMT(self.project)


















