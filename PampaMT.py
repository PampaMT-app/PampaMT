#!/usr/bin/python3
#coding: utf-8

"""
    This Software was developed for to processing data Magnetotelluric.
"""

# Version for Linux

# Developed by Patrick Rogger Garcia
# E-mail: patrick_rogger@hotmail.com

__author__ = 'Patrick Rogger Garcia'
__email__ = 'patrick_rogger@hotmail.com'
__version__ = '0.0.1'
__status__ = 'Production'


# Packages import
import kivy
import os
import pickle
import glob
import sys
import threading
from time import sleep
#import pygame
from shutil import copyfile

# Api Kivy Minimum Requirement
kivy.require('1.9.0')

# Set USER

user = os.environ['HOME']

# Setting the Language
# Read file file/set_language
print('Setting Language ...')
arq_set_lang = open(user + '/.PampaMT/file/set_language', 'r')
set_lang = arq_set_lang.read()
arq_set_lang.close()
print('Language --> ' + set_lang)



# Default en_US
print('Opening Dictionary ...')
arq_lang = open('dic/' + set_lang, 'rb')
lang = pickle.load(arq_lang)
arq_lang.close()

# Convention for all code
# Objects:
#       bt_...   -> Button()
#       bl_...   -> Label()
#       lay_...  -> Layout()

print('Opening Log ...')
arq_log = open('dic/logNot_' + set_lang, 'rb')
logNot = pickle.load(arq_log)
arq_log.close()



# Packages import GUI
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty

# Packages import Widgets
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

# Packages import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from math import sqrt

# Packages PampaMT
from source.site import Site
from source.windowsite import FilePPLT, make_file_pplt, save_file_pplt
from source.project import ProjectPPMT, read_ppmt_file, ErrorLoading, save
from source.tools.sorted_t import sorted_t
from source.tools.plotZ import export_matplotlib_jones

from source.plot import *

from source.kivy_pampamt.buttonpampamt import ButtonBlack

# Open project
arq_file_main_exec = open(user + '/.PampaMT/file/file_exec_main', 'r')
path_file_ppmt = arq_file_main_exec.readline()
arq_file_main_exec.close()



try:
    project = read_ppmt_file(path_file_ppmt)
except EOFError:

    window = ErrorLoading()
    Window.size = 300, 100
    window.run()

def mod(x):
    x_2 = x**2
    return sqrt(x_2)


for site_last in project.sites:
    if project.last_edit_site == site_last.name:
        site = site_last
        break
try:
    print('Site Select: ' + site.name)
except NameError:
    project.last_edit_site = project.sites[0].name
    site = project.sites[0]
    print('Site Select: ' + site.name)

path_dir_ppmt = path_file_ppmt.replace('/' + project.name + '.ppmt', '')

class LabelDivX(Label):
    pass

class FilePPLTSelect(Button):
    cor_no = [.25, .25, .25, 1.]
    cor = [0, 0, 0, 1.]
    active = False
    active_n = 0
    n = -1

    def __init__(self, object_pplt, **kwargs):
        super(FilePPLTSelect, self).__init__(**kwargs)

        self.obj_pplt = object_pplt
        self.text = self.obj_pplt.rate + '/' + self.obj_pplt.name
        self.background_normal = ' '
        self.size_hint = None, None
        self.border = [0, 0, 0, 0]
        self.height = 25
        if self.obj_pplt.band == '65536H' or self.obj_pplt.band == '4096H':
            self.width = 300
        else:
            self.width = 250
        self.background_color = self.cor_no
        self.on_press = self.select

    def select(self):
        self.background_color = self.cor
        self.on_press = self.no_select
        self.active = True
        self.active_n = 1

        self.obj_pplt.active_file = True
        arq_save = open('PampaMT/file_pplt/' + site.name + '/' + self.obj_pplt.rate + '_' + self.obj_pplt.name_plot, 'wb')
        pickle.dump(self.obj_pplt, arq_save)
        arq_save.close()


        print('active: ' + str(self.active))

    def no_select(self):
        self.background_color = self.cor_no
        self.on_press = self.select
        self.active = False
        self.active_n = 0

        self.obj_pplt.active_file = False
        arq_save = open('PampaMT/file_pplt/' + site.name + '/' + self.obj_pplt.rate + '_' + self.obj_pplt.name_plot, 'wb')
        pickle.dump(self.obj_pplt, arq_save)
        arq_save.close()

        print('active: ' + str(self.active))



class ScrollBox(BoxLayout):
    pass


class BandLay(BoxLayout):
    def __init__(self, **kwargs):
        super(BandLay, self).__init__(**kwargs)

        self.tab_item = TabbedPanel()
        self.tab_item.do_default_tab = False
        self.tab_item.tab_height = 20

        list_bands = []
        if site.equipment == 'ADU06':
            list_bands = ['A', 'B', 'F', 'C', 'D']
        elif site.equipment == 'ADU07':
            list_bands = ['65536H', '4096H', '128H', '4H']

        for band in list_bands:
            tab_item = TabbedPanelItem()
            tab_item.text = band
            self.tab_item.add_widget(tab_item)

            list_file_pplt = self.search_pplt_file(band)
            site.files_plot[band] = list_file_pplt

            self.grid_lay = ScrollBox()

            i = 0
            for file_pplt_select in site.files_plot[band]:

                self.grid_lay.ids.grid.add_widget(file_pplt_select)
                print(file_pplt_select.obj_pplt.name)
                i += 1

            if band == '65536H' or band == '4096H':
                self.grid_lay.ids.grid.size_hint_x = None
                self.grid_lay.ids.grid.width = int(i / 3 * 300)
            else:
                self.grid_lay.ids.grid.size_hint_x = None
                self.grid_lay.ids.grid.width = int(i/3 * 250)

            tab_item.add_widget(self.grid_lay)
        self.add_widget(self.tab_item)


        print(project.path_file_ppmt)











    def search_pplt_file(self, band):

        list_path_band_pplt = glob.glob('PampaMT/file_pplt/' + site.name + '/*' + band + '*')
        list_path_band_pplt = sorted(list_path_band_pplt)

        list_file_pplt = []
        for path_file_ppmt in list_path_band_pplt:
            arq_pplt = open(path_file_ppmt, 'rb')
            file_pplt = pickle.load(arq_pplt)
            arq_pplt.close()

            file_pplt_select = FilePPLTSelect(object_pplt=file_pplt)

            if file_pplt.active_file == True:
                file_pplt_select.select()


            list_file_pplt.append(file_pplt_select)

        return list_file_pplt


class LaySelectPlot(FloatLayout):
    # ----------------------------------- Cursor e selecao dos Pontos -----------------------------------
    pos_i = ()
    pos_f = ()
    pos_i_x = 0
    pos_i_y = 0
    size_x = 0
    size_y = 0



    def on(self, intancia, value):
        if self.test_press_select_period:
            self.pos_i = value.pos
            self.pos_i_x = value.pos[0]
            self.pos_i_y = value.pos[1]

    def up(self, instancia, value):

        if self.test_press_select_period:
            self.pos_f = value.pos
            self.canvas.before.clear()
            self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))
            self.canvas.before.add(Color(rgba=[1., 1., 1., 1.]))

            if (mod(self.size_x) > 5) or (mod(self.size_y) > 5):

                for i in self.list_bt_plot:
                    pos_x = i.x
                    pos_y = i.y

                    coor_i_x = [self.pos_i_x, self.pos_i_x - self.size_x]

                    coor_x = sorted(coor_i_x)

                    coor_i_y = [self.pos_i_y, self.pos_i_y - self.size_y]
                    coor_y = sorted(coor_i_y)

                    if ((pos_x > coor_x[0]) and (pos_x < coor_x[1]) and (pos_y > coor_y[0]) and (
                            pos_y < coor_y[1])):

                        if i.active == False:
                            i.select()
                        else:
                            i.no_select()

            self.size_x = 0
            self.size_y = 0

    def move(self, instancia, value):

        if self.test_press_select_period:
            self.size_x = self.pos_i_x - value.pos[0]
            self.size_y = self.pos_i_y - value.pos[1]

            if (mod(self.size_x) > 5) or (mod(self.size_y) > 5):
                self.canvas.before.clear()
                self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))
                self.canvas.before.add(Color(rgba=[1., 1., 1., 1.]))
                self.canvas.before.add(Color(rgba=[0, 0, 0, .2]))
                self.canvas.before.add(
                    Rectangle(pos=(self.pos_i_x, self.pos_i_y), size=(-self.size_x, -self.size_y)))


    def __init__(self, **kwargs):
        super(LaySelectPlot, self).__init__(**kwargs)

        self.test_press_select_period = False
        self.list_bt_plot = []

        self.bind(on_touch_down=self.on)
        self.bind(on_touch_up=self.up)
        self.bind(on_touch_move=self.move)

        self.size_hint = None, None
        self.height = 450
        self.width = 650
        self.pos = 0, 200

        self.canvas.before.add(Color(rgba=[0, 0, 0, 1.]))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

class ViewFileActive(BoxLayout):
    pass

class ScreenSuper(BoxLayout):

    lang_site_edit = site.name
    lang_file = lang['File_Bar']
    lang_new_project = lang['New_project']
    lang_open_project = lang['Open_project']
    lang_restore_project = lang['Restore_Project']
    lang_view_all_project = lang['View_all_Project']
    lang_set_project = lang['Set_Project']
    lang_exit = lang['Exit']

    lang_site = lang['Site']
    lang_add_site = lang['Add_Site']
    lang_remove_site = lang['Remove_Site']
    lang_add_data_file = lang['Add_Data_File']
    lang_set_site = lang['Set_Site']
    lang_change_site = lang['Change_Site']

    lang_tools = lang['Tools']
    lang_rhoplus = lang['Rhoplus']
    lang_convert_format = lang['Convert_Format']
    lang_bash_console = lang['Bash_Console']

    lang_settings = lang['Settings']
    lang_language = lang['Language']

    lang_view = lang['View']
    lang_time_series = lang['Time_Series']
    lang_pseudo_section = lang['Pseudo_Section']
    lang_map_stations = lang['Map_Stations']

    lang_export = lang['Export']
    lang_figure_station = lang['Figure_Station']

    lang_help = lang['Help']
    lang_about = lang['About']
    lang_tutorial = lang['Tutorial']
    lang_update = lang['Update']

    lang_select_site = lang['Select_Site']
    lang_tojone = lang['Tojones']

    lang_select_period = lang['Select_Period']
    lang_set_color = lang['Set_Color']
    lang_change_view = lang['Change_View']


    x0rho = 50
    y0rho = 225

    min_exp_rho = 2

    fzoomrho = 60
    dx_rho = 480
    dy_rho = 360

    x0phi = x0rho + dx_rho + 50
    y0phi = y0rho
    fzoomyphi = 1.1
    fzoomphi = 37

    fzoomZ = 37
    fzoomyZ = 6.5

    list_bt_plot = []


    press_icon = True

    def open_sites_in_bar(self):

        if self.press_icon == True:
            self.ids.scroll_view.height = 30
            self.press_icon = False

        elif self.press_icon == False:
            self.ids.scroll_view.height = 0
            self.press_icon = True

    def close_open_site(self, instance):
        print('close open')
        print('Select: ' + instance.text)
        project.last_edit_site = instance.text

        project_save = project
        for site in project_save.sites:
            site.files_plot = {}



        save(project_save)

        window.get_running_app().stop()
        Window.close()
        os.chdir(user + '/.PampaMT')
        os.system('./PampaMT.py')

    def open_not_implemented(self, log, pop_width, pop_height):
        pop = Popup(title=lang['Not_yet_implemented'])
        pop.size_hint = None, None
        pop.width = pop_width
        pop.height = pop_height
        pop.content = Label(text=logNot[log])
        pop.open()

    def open_rhoplus(self):
        os.system('rhoplusGUI')

    press_box_set_color = True
    def on_press_set_color(self):

        if self.press_box_set_color == True:
            self.list_active_file_pplt = []
            self.ids.box_lay_set_color.width = 350
            self.press_box_set_color = False

            for band in site.files_plot.keys():
                for file_pplt in site.files_plot[band]:
                   if file_pplt.active == True:
                       self.list_active_file_pplt.append(file_pplt)

            for file_pplt in self.list_active_file_pplt:


                bt_file_pplt = ButtonBlack()
                bt_file_pplt.text = file_pplt.obj_pplt.rate + '/' + file_pplt.obj_pplt.name

                bt_file_pplt.file_pplt = file_pplt
                bt_file_pplt.bind(on_press=self.set_color)
                bt_file_pplt.width = 350
                bt_file_pplt.height = 25

                self.ids.box_list_color.add_widget(bt_file_pplt)
                self.ids.box_list_color.height = len(self.list_active_file_pplt) * 25



        else:
            self.ids.box_lay_set_color.width = 0
            self.press_box_set_color = True
            self.ids.box_list_color.clear_widgets()

    def set_color(self, instance):

        self.bt_selection_color_edit = instance
        self.ids.color_select.color = instance.file_pplt.obj_pplt.color
        instance.color = [1., 0, 0, 1.]


    def on_press_plot(self):

        self.ids.plot_1_point.clear_widgets()
        self.ids.plot_2_point.clear_widgets()
        self.list_active_file_pplt = []
        for band in site.files_plot.keys():
            for file_pplt in site.files_plot[band]:
                if file_pplt.active == True:
                    self.list_active_file_pplt.append(file_pplt)

        self.list_bt_plot = []

        self.box_view_select.clear_widgets()
        j = 0
        for file_pplt in self.list_active_file_pplt:
            i = 0
            coor_pixel_file_pplt = self.read_file_pplt_to_coord_pixel(file_pplt)
            for T in file_pplt.obj_pplt.activated:

                bt_rho_xy = PointPlot(pos=[coor_pixel_file_pplt[0][i], coor_pixel_file_pplt[1][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_rho_xy.cor = file_pplt.obj_pplt.color
                bt_rho_xy.n = i+1

                bt_rho_yx = PointPlotCirc(pos=[coor_pixel_file_pplt[0][i], coor_pixel_file_pplt[2][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_rho_yx.cor = file_pplt.obj_pplt.color

                bt_phi_xy = PointPlot(pos=[coor_pixel_file_pplt[3][0][i], coor_pixel_file_pplt[3][1][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_phi_xy.cor = file_pplt.obj_pplt.color
                bt_phi_xy.height = 4
                bt_phi_xy.width = 4

                bt_phi_yx = PointPlotCirc(pos=[coor_pixel_file_pplt[4][0][i], coor_pixel_file_pplt[4][1][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_phi_yx.cor = file_pplt.obj_pplt.color
                bt_phi_yx.height = 4
                bt_phi_yx.width = 4

                bt_RZ_xx = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[6][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_RZ_xx.cor = file_pplt.obj_pplt.color
                bt_RZ_xx.height = 4
                bt_RZ_xx.width = 4

                bt_IZ_xx = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[7][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_IZ_xx.cor = file_pplt.obj_pplt.color
                bt_IZ_xx.height = 4
                bt_IZ_xx.width = 4

                bt_RZ_xy = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[8][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_RZ_xy.cor = file_pplt.obj_pplt.color
                bt_RZ_xy.height = 4
                bt_RZ_xy.width = 4

                bt_IZ_xy = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[9][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_IZ_xy.cor = file_pplt.obj_pplt.color
                bt_IZ_xy.height = 4
                bt_IZ_xy.width = 4

                bt_RZ_yx = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[10][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_RZ_yx.cor = file_pplt.obj_pplt.color
                bt_RZ_yx.height = 4
                bt_RZ_yx.width = 4

                bt_IZ_yx = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[11][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_IZ_yx.cor = file_pplt.obj_pplt.color
                bt_IZ_yx.height = 4
                bt_IZ_yx.width = 4

                bt_RZ_yy = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[12][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_RZ_yy.cor = file_pplt.obj_pplt.color
                bt_RZ_yy.height = 4
                bt_RZ_yy.width = 4

                bt_IZ_yy = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[13][i]], file_pplt=file_pplt.obj_pplt, i=i)
                bt_IZ_yy.cor = file_pplt.obj_pplt.color
                bt_IZ_yy.height = 4
                bt_IZ_yy.width = 4

                bt_rho_xy.points_inte = [bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]
                bt_rho_yx.points_inte = [bt_rho_xy, bt_rho_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]

                bt_phi_xy.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]
                bt_phi_yx.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]

                bt_RZ_xx.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]
                bt_IZ_xx.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]

                bt_RZ_xy.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]
                bt_IZ_xy.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]

                bt_RZ_yx.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_IZ_yx, bt_RZ_yy, bt_IZ_yy]
                bt_IZ_yx.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_RZ_yy, bt_IZ_yy]

                bt_RZ_yy.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_IZ_yy]
                bt_IZ_yy.points_inte = [bt_rho_xy, bt_rho_yx, bt_phi_xy, bt_phi_yx, bt_RZ_xx, bt_IZ_xx, bt_RZ_xy, bt_IZ_xy, bt_RZ_yx, bt_IZ_yx, bt_RZ_yy]


                if T:
                    bt_rho_xy.select()
                    bt_rho_yx.select()
                    bt_phi_xy.select()
                    bt_phi_yx.select()

                    bt_RZ_xx.select()
                    bt_IZ_xx.select()
                    bt_RZ_xy.select()
                    bt_IZ_xy.select()
                    bt_RZ_yx.select()
                    bt_IZ_yx.select()
                    bt_RZ_yy.select()
                    bt_IZ_yy.select()


                    self.ids.plot_1_point.add_widget(bt_rho_xy)
                    self.ids.plot_1_point.add_widget(bt_rho_yx)
                    self.ids.plot_1_point.add_widget(bt_phi_xy)
                    self.ids.plot_1_point.add_widget(bt_phi_yx)
                    self.ids.plot_2_point.add_widget(bt_RZ_xx)
                    self.ids.plot_2_point.add_widget(bt_IZ_xx)
                    self.ids.plot_2_point.add_widget(bt_RZ_xy)
                    self.ids.plot_2_point.add_widget(bt_IZ_xy)
                    self.ids.plot_2_point.add_widget(bt_RZ_yx)
                    self.ids.plot_2_point.add_widget(bt_IZ_yx)
                    self.ids.plot_2_point.add_widget(bt_RZ_yy)
                    self.ids.plot_2_point.add_widget(bt_IZ_yy)

                    self.list_bt_plot.append(bt_rho_xy)
                i += 1
            j += 1

            lb_view_select = Label()
            lb_view_select.size_hint_y = None
            lb_view_select.height = 30

            lb_view_select.text = file_pplt.obj_pplt.rate + '/' + file_pplt.obj_pplt.name
            lb_view_select.color = file_pplt.obj_pplt.color

            self.box_view_select.add_widget(lb_view_select)
            self.box_view_select.add_widget(LabelDivX())
        self.box_view_select.height = int(j*31)

    test_press_select_period = False
    test_press_select_period_plot = True
    def on_press_select_period(self):

        if self.test_press_select_period_plot == True:

            #parallel_progress_bar = threading.Thread(target=self.start_progress_bar)
            #parallel_progress_bar.start()



            self.ids.bt_select_period.text = lang['Finish']
            self.test_press_select_period = True
            self.list_bt_plot = []

            self.ids.plot_1_point.clear_widgets()
            self.ids.plot_2_point.clear_widgets()

            self.list_active_file_pplt = []

            self.lay_select = LaySelectPlot()
            self.lay_select.test_press_select_period = self.test_press_select_period
            self.lay_select.list_bt_plot = self.list_bt_plot
            self.ids.plot_1_point.add_widget(self.lay_select)


            for band in site.files_plot.keys():
                for file_pplt in site.files_plot[band]:
                    if file_pplt.active == True:
                        self.list_active_file_pplt.append(file_pplt)

            for file_pplt in self.list_active_file_pplt:
                i = 0
                coor_pixel_file_pplt = self.read_file_pplt_to_coord_pixel(file_pplt)
                for T in file_pplt.obj_pplt.activated:

                    bt_rho_xy = PointPlot(pos=[coor_pixel_file_pplt[0][i], coor_pixel_file_pplt[1][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_rho_xy.cor = file_pplt.obj_pplt.color

                    bt_rho_yx = PointPlotCirc(pos=[coor_pixel_file_pplt[0][i], coor_pixel_file_pplt[2][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_rho_yx.cor = file_pplt.obj_pplt.color


                    bt_phi_xy = PointPlot(pos=[coor_pixel_file_pplt[3][0][i], coor_pixel_file_pplt[3][1][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_phi_xy.cor = file_pplt.obj_pplt.color
                    bt_phi_xy.height = 4
                    bt_phi_xy.width = 4

                    bt_phi_yx = PointPlotCirc(pos=[coor_pixel_file_pplt[4][0][i], coor_pixel_file_pplt[4][1][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_phi_yx.cor = file_pplt.obj_pplt.color
                    bt_phi_yx.height = 4
                    bt_phi_yx.width = 4

                    bt_RZ_xx = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[6][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_RZ_xx.cor = file_pplt.obj_pplt.color
                    bt_RZ_xx.height = 4
                    bt_RZ_xx.width = 4

                    bt_IZ_xx = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[7][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_IZ_xx.cor = file_pplt.obj_pplt.color
                    bt_IZ_xx.height = 4
                    bt_IZ_xx.width = 4

                    bt_RZ_xy = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[8][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_RZ_xy.cor = file_pplt.obj_pplt.color
                    bt_RZ_xy.height = 4
                    bt_RZ_xy.width = 4

                    bt_IZ_xy = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[9][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_IZ_xy.cor = file_pplt.obj_pplt.color
                    bt_IZ_xy.height = 4
                    bt_IZ_xy.width = 4

                    bt_RZ_yx = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[10][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_RZ_yx.cor = file_pplt.obj_pplt.color
                    bt_RZ_yx.height = 4
                    bt_RZ_yx.width = 4

                    bt_IZ_yx = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[11][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_IZ_yx.cor = file_pplt.obj_pplt.color
                    bt_IZ_yx.height = 4
                    bt_IZ_yx.width = 4

                    bt_RZ_yy = PointPlot(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[12][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_RZ_yy.cor = file_pplt.obj_pplt.color
                    bt_RZ_yy.height = 4
                    bt_RZ_yy.width = 4

                    bt_IZ_yy = PointPlotCirc(pos=[coor_pixel_file_pplt[5][i], coor_pixel_file_pplt[13][i]], file_pplt=file_pplt.obj_pplt, i=i)
                    bt_IZ_yy.cor = file_pplt.obj_pplt.color
                    bt_IZ_yy.height = 4
                    bt_IZ_yy.width = 4


                    if T:
                        bt_rho_xy.select()
                        bt_rho_yx.select()
                        bt_phi_xy.select()
                        bt_phi_yx.select()

                        bt_RZ_xx.select()
                        bt_IZ_xx.select()

                        bt_RZ_xy.select()
                        bt_IZ_xy.select()

                        bt_RZ_yx.select()
                        bt_IZ_yx.select()

                        bt_RZ_yy.select()
                        bt_IZ_yy.select()

                    self.ids.plot_1_point.add_widget(bt_rho_xy)
                    self.ids.plot_1_point.add_widget(bt_rho_yx)
                    self.ids.plot_1_point.add_widget(bt_phi_xy)
                    self.ids.plot_1_point.add_widget(bt_phi_yx)
                    self.ids.plot_2_point.add_widget(bt_RZ_xx)
                    self.ids.plot_2_point.add_widget(bt_IZ_xx)
                    self.ids.plot_2_point.add_widget(bt_RZ_xy)
                    self.ids.plot_2_point.add_widget(bt_IZ_xy)
                    self.ids.plot_2_point.add_widget(bt_RZ_yx)
                    self.ids.plot_2_point.add_widget(bt_IZ_yx)
                    self.ids.plot_2_point.add_widget(bt_RZ_yy)
                    self.ids.plot_2_point.add_widget(bt_IZ_yy)
                    self.list_bt_plot.append(bt_rho_xy)
                    self.list_bt_plot.append(bt_rho_yx)
                    self.list_bt_plot.append(bt_phi_xy)
                    self.list_bt_plot.append(bt_phi_yx)
                    self.list_bt_plot.append(bt_RZ_xx)
                    self.list_bt_plot.append(bt_IZ_xx)
                    self.list_bt_plot.append(bt_RZ_xy)
                    self.list_bt_plot.append(bt_IZ_xy)
                    self.list_bt_plot.append(bt_RZ_yx)
                    self.list_bt_plot.append(bt_IZ_yx)
                    self.list_bt_plot.append(bt_RZ_yy)
                    self.list_bt_plot.append(bt_IZ_yy)

                    i += 1

            self.lay_select.list_bt_plot = self.list_bt_plot
            self.test_press_select_period_plot = False
        else:
            self.ids.bt_select_period.text = self.lang_select_period
            self.lay_select.test_press_select_period = False
            self.test_press_select_period_plot =True
            self.test_press_select_period = False
            self.on_press_plot()


    def read_file_pplt_to_coord_pixel(self, file_pplt):

        T = []

        rhoxy = []
        rhoyx = []

        phixy = [[], []]
        phiyx = [[], []]

        TZ = []

        RZxx = []
        RZxy = []
        RZyx = []
        RZyy = []

        IZxx = []
        IZxy = []
        IZyx = []
        IZyy = []

        for period in file_pplt.obj_pplt.T:
            T.append(coorlog_to_pixel(coor=period, v0=self.x0rho, fzoom=self.fzoomrho, exp_min=4))

        for rho in file_pplt.obj_pplt.rhoxy[0]:
            rhoxy.append(coorlog_to_pixel(coor=rho, v0=self.y0rho, fzoom=self.fzoomrho, exp_min=self.min_exp_rho))

        for rho in file_pplt.obj_pplt.rhoyx[0]:
            rhoyx.append(coorlog_to_pixel(coor=rho, v0=self.y0rho, fzoom=self.fzoomrho, exp_min=self.min_exp_rho))

        i = 0
        for phi in file_pplt.obj_pplt.phixy[0]:
            phixy[0].append(coorlog_to_pixel(coor=file_pplt.obj_pplt.T[i], v0=self.x0phi, fzoom=self.fzoomphi, exp_min=4))
            phixy[1].append(int((phi * self.fzoomyphi) + self.y0phi))
            i += 1

        i = 0
        for phi in file_pplt.obj_pplt.phiyx[0]:
            phiyx[0].append(coorlog_to_pixel(coor=file_pplt.obj_pplt.T[i], v0=self.x0phi, fzoom=self.fzoomphi, exp_min=4))
            phiyx[1].append(int(((phi+180) * self.fzoomyphi) + self.y0phi))
            i += 1

        for period in file_pplt.obj_pplt.T:
            TZ.append(coorlog_to_pixel(coor=period, v0=self.ids.plot_2.x + 20, fzoom=self.fzoomZ, exp_min=4))

        for RZ in file_pplt.obj_pplt.RZxx[0]:
            RZxx.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + RZ)+840))

        for IZ in file_pplt.obj_pplt.IZxx[0]:
            IZxx.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + IZ)+840))

        for RZ in file_pplt.obj_pplt.RZxy[0]:
            RZxy.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + RZ)+570))

        for IZ in file_pplt.obj_pplt.IZxy[0]:
            IZxy.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + IZ)+570))

        for RZ in file_pplt.obj_pplt.RZyx[0]:
            RZyx.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + RZ)+300))

        for IZ in file_pplt.obj_pplt.IZyx[0]:
            IZyx.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + IZ)+300))

        for RZ in file_pplt.obj_pplt.RZyy[0]:
            RZyy.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + RZ)+30))

        for IZ in file_pplt.obj_pplt.IZyy[0]:
            IZyy.append(int((self.ids.plot_2.x+20) + self.fzoomyZ*(15 + IZ)+30))



        return T, rhoxy, rhoyx, phixy, phiyx, TZ, RZxx, IZxx, RZxy, IZxy, RZyx, IZyx, RZyy, IZyy


    def set_color_ok(self):


        file_pplt = self.bt_selection_color_edit.file_pplt.obj_pplt

        color = list(self.ids.color_select.color)
        print(color)

        self.bt_selection_color_edit.file_pplt.obj_pplt.color = color

        arq_save = open('PampaMT/file_pplt/' + site.name + '/' + self.bt_selection_color_edit.file_pplt.obj_pplt.rate + '_' + self.bt_selection_color_edit.file_pplt.obj_pplt.name_plot, 'wb')
        pickle.dump(file_pplt, arq_save)
        arq_save.close()

        self.bt_selection_color_edit.color = [1., 1., 1., 1.]
        self.on_press_plot()
        self.on_press_set_color()




    def start_progress_bar(self):

        for i in range(100):
            self.ids.progress_bar.value = i


    def close_selected_two_equal_periods(self):
        sleep(3)
        self.ids.plot_1.remove_widget(self.bt_select_two)

    def on_press_bt_selected_two_equal_periods(self):
        popup = ModalView(size_hint=(None,None))
        popup.add_widget(Label(text=lang['Selected_two_equal_periods'],size_hint=(None,None),height=30, width=300))
        popup.height = 40
        popup.width = 300
        popup.open()
        print('selected two equal periods')

    def tojones(self):

        self.popup_tojones.dismiss()
        os.system('tojones final/' + site.name +'/selection.dat > final/' + self.tb_jones.text)

        if os.path.isdir(path_dir_ppmt + '/jones_dat'):
            pass
        else:
            os.mkdir(path_dir_ppmt + '/jones_dat')

        copyfile('final/' + self.tb_jones.text, path_dir_ppmt + '/jones_dat/' + self.tb_jones.text)



    def on_press_tojones(self):
        if os.path.isdir(user + '/PampaMT/PROC_MT/' + project.name + '/final/' + site.name):
            print('final/site existe')
        else:
            os.mkdir(user + '/PampaMT/PROC_MT/' + project.name + '/final/' + site.name)
            print('Make /final/' + site.name)

        arq_file_select_periods = open(user + '/PampaMT/PROC_MT/'+ project.name + '/final/' + site.name + '/selection.dat', 'w')

        #print(self.list_bt_plot)

        line_write_0 = '# coord {:.5f} {:.5f} {:.0f}\n'.format(site.coordinates['Longitude'], site.coordinates['Latitude'], site.coordinates['Elevation'])
        #print(line_write_0)

        arq_file_select_periods.writelines(line_write_0)

        status, list_sorted_plot, bt_plot_error = sorted_t(self.list_bt_plot)
        #print(list_sorted_plot)

        if status == True:
            print('Error Tojones')
            self.bt_select_two = Button(text='!', size_hint=(None, None))
            self.bt_select_two.on_press = self.on_press_bt_selected_two_equal_periods
            self.bt_select_two.height = 10
            self.bt_select_two.width = 10
            self.bt_select_two.center_x = bt_plot_error.x
            self.bt_select_two.center_y = bt_plot_error.y + 30

            self.ids.plot_1.add_widget(self.bt_select_two)
            arq_file_select_periods.close()
            close_bt_select_two = threading.Thread(target=self.close_selected_two_equal_periods)
            close_bt_select_two.start()
        else:
            for bt_plot in list_sorted_plot:

                line_write = bt_plot.obj_file.rate + '/' + bt_plot.obj_file.name + ' [' + str(bt_plot.n) + '-' +  str(bt_plot.n) + ']\n'
                arq_file_select_periods.writelines(line_write)

            arq_file_select_periods.close()

            self.popup_tojones = ModalView(size_hint=(None,None))
            self.popup_tojones.height = 90
            self.popup_tojones.width = 320

            lay = BoxLayout(size_hint=(None, None), height=70, width=300)
            lay.orientation = 'vertical'

            lay.spacing = 5
            self.tb_jones = TextInput()
            self.tb_jones.text = site.name + '.dat'
            self.tb_jones.multiline = False
            self.tb_jones.on_text_validate = self.tojones
            lay.add_widget(self.tb_jones)

            bt_save_jones = Button(text=lang['Save'])
            bt_save_jones.on_press = self.tojones
            lay.add_widget(bt_save_jones)


            self.popup_tojones.add_widget(lay)
            self.popup_tojones.open()

















    def __init__(self, **kwargs):
        super(ScreenSuper, self).__init__(**kwargs)
        os.chdir(user + '/PampaMT/PROC_MT/' + project.name)
        print(site.files_plot)


        for site_i in project.sites:
            bt_site = Button()
            bt_site.text = site_i.name
            bt_site.size_hint_x = None
            bt_site.width = 100
            bt_site.size_hint_y = None
            bt_site.height = 30
            bt_site.bind(on_press=self.close_open_site)
            if site_i.name == site.name:
                bt_site.background_normal = ''
                bt_site.background_color = [.2, .2, .2, 1]



            self.ids.box_lay_sites.width = len(project.sites) * 100
            self.ids.box_lay_sites.add_widget(bt_site)


        box_band = BandLay()
        self.ids.box_window.add_widget(box_band)

        grafic_lines_rho = draws_lines_rho(x0=self.x0rho, y0=self.y0rho, dx=self.dx_rho, dy=self.dy_rho,
                                       fzoom=self.fzoomrho, border=1.05, xmin=-4, xmax=4, ymin=-self.min_exp_rho, ymax=4,
                                       limx=100000000, limy=1000000, label_y=True)

        grafic_lines_phi = draws_lines_phi(x0=self.x0phi, fzoomy=self.fzoomyphi, y0=self.y0phi, dx=300, dy=200,
                                         fzoom=self.fzoomphi, border=1.05, xmin=-4, xmax=4, ymin=0, ymax=180,
                                         limx=100000000, limy=180, label_y=True, scale_y=True)


        self.y0Z = self.ids.plot_2.y


        grafic_lines_zxx = draws_lines_Z(x0=self.ids.plot_2.x + 20,fzoomy=self.fzoomyZ, y0=self.y0Z + 840, dx=300, dy=200,
                                       fzoom=self.fzoomZ, border=1.05, xmin=-4, xmax=4, ymin=0, ymax=35,
                                       limx=100000000, limy=90, label_y=True, scale_y=True, component='xx')

        grafic_lines_zxy = draws_lines_Z(x0=self.ids.plot_2.x + 20, fzoomy=self.fzoomyZ, y0=self.y0Z + 570, dx=300, dy=200,
                                         fzoom=self.fzoomZ, border=1.05, xmin=-4, xmax=4, ymin=0, ymax=35,
                                         limx=100000000, limy=90, label_y=True, scale_y=True, component='xy')

        grafic_lines_zyx = draws_lines_Z(x0=self.ids.plot_2.x + 20, fzoomy=self.fzoomyZ, y0=self.y0Z + 300, dx=300, dy=200,
                                         fzoom=self.fzoomZ, border=1.05, xmin=-4, xmax=4, ymin=0, ymax=35,
                                         limx=100000000, limy=90, label_y=True, scale_y=True, component='yx')

        grafic_lines_zyy = draws_lines_Z(x0=self.ids.plot_2.x + 20, fzoomy=self.fzoomyZ, y0=self.y0Z + 30, dx=300, dy=200,
                                         fzoom=self.fzoomZ, border=1.05, xmin=-4, xmax=4, ymin=0, ymax=35,
                                         limx=100000000, limy=90, label_y=True, scale_y=True, component='yy')




        self.ids.plot_1.add_widget(grafic_lines_rho)
        self.ids.plot_1.add_widget(grafic_lines_phi)
        self.ids.plot_2.add_widget(grafic_lines_zxx)
        self.ids.plot_2.add_widget(grafic_lines_zxy)
        self.ids.plot_2.add_widget(grafic_lines_zyx)
        self.ids.plot_2.add_widget(grafic_lines_zyy)

        lay_select = ViewFileActive()

        self.box_view_select = lay_select.ids.lay_view_file_active

        lay_select.pos = self.x0phi, self.y0phi + 200 + 25
        # with self.box_view_select.canvas:
        #     Color(rgba=[.8, .8, .8, 1.])
        #     Rectangle(size=self.box_view_select.size, pos=self.box_view_select.pos)

        self.ids.plot_1.add_widget(lay_select)

        self.on_press_plot()




class PampaMT(App):
    def build(self):
        return ScreenSuper()

window = PampaMT()
window.icon = user + '/.PampaMT/image/icon.png'
window.title = 'PampaMT -- ' + project.name
Window.size = 1300, 750


if __name__ == '__main__':
    print('Start PampaMT')
    window.run()

