#!/usr/bin/python3
#coding: utf-8

"""
    This Software was developed for to processing data Magnetotellurics.
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
import time
from timeit import default_timer as timer
import threading
#import pygame

# API Kivy Minimum Requirement
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
arg_lang = open('dic/' + set_lang, 'rb')
lang = pickle.load(arg_lang)
arg_lang.close()

# Var global
path_new_dir = ' '

# Convention for all code
# Objects:
#       bt_...   -> Button()
#       bl_...   -> Label()
#       lay_...  -> Layout()



# Packages import GUI
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty

# Packages import Widgets
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar

# Packages Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

# Packages Kivy/PampaMT
from source.kivy_pampamt.buttonpampamt import ButtonBlack
from source.kivy_pampamt.popuppampamt import PopupPampaMT
from source.kivy_pampamt.popuppampamtloading import PopUpLoading

# Packages PampaMT
from source.site import Site
from source.processingZ import ProcessingZ
from source.project import ProjectPPMT, read_ppmt_file, save
from source.tools.read_ats_coordenates import read_ats_coordinates
from source.windowsite import FilePPLT, make_file_pplt, save_file_pplt

# tirar depoius
from source.project import ProjectTeste

# Canvas
from kivy.graphics import Rectangle, Color

# Class Button Open/ New Project/ Close
class ButtonNewOpen(BoxLayout):

    # Functions
    new_proj = ObjectProperty(None)
    open_proj = ObjectProperty(None)


    def __init__(self,**kwargs):
        super(ButtonNewOpen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5

        # Button >New Project<
        bt_new_project = ButtonBlack(text=lang['New_project'])
        bt_new_project.on_press = self.new_proj
        bt_new_project.pos_hint = {'center_x': .5, 'center_y': .5}
        self.add_widget(bt_new_project)


        # Button >Open Project<
        bt_open_project = ButtonBlack(text=lang['Open_project'])
        bt_open_project.on_press = self.open_proj
        bt_open_project.pos_hint = {'center_x': .5, 'center_y': .5}
        self.add_widget(bt_open_project)

# Class Window create a new path project
class FileSave(BoxLayout):


    # Functions Windows
    save_new_project = ObjectProperty(None)
    cancel = ObjectProperty(None)
    back_to = ObjectProperty(None)
    new_dir = ObjectProperty(None)

    # Language
    text_button_save = lang['Save']
    text_button_cancel = lang['Cancel']
    text_button_back = lang['Back']
    text_new_project = lang['New_project']


# Class Window select sites
class SelecSite(BoxLayout):

    # Functions
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

    # Language
    lb_selec_the_sites = lang['Select_the_sites']
    lb_Select_Directory_with_all_Sites = lang['Select_Directory_with_all_Sites']
    bt_select = lang['Select']
    bt_cancel = lang['Cancel']


# Class popup to create new site
class PopupNewSite(BoxLayout):

    make_new_site = ObjectProperty(None)


class PopupConvertBinAsc(BoxLayout):

    bt_cancel = lang['Cancel']
    lb_convert = lang['Convert_bin_format_to_asc']

    bt_ok = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SelectAutoFillSites(BoxLayout):

    # Lang
    lb_automatic_site_selection = lang['Automatic_Site_Selection']
    lb_Directory_path_containing_all_sites = lang['Directory_path_containing_all_sites']
    lb_Structure = lang['Structure']
    lb_path_all_site = lang['path_all_site_site']
    lb_equipment = lang['Equipment']
    bt_cancel = lang['Cancel']
    lb_path_all_site_site = lang['path_all_site_site'] + '/site/'

    # Function
    open_search_path_all_site = ObjectProperty(None)
    cancel = ObjectProperty(None)
    auto_fill = ObjectProperty(None)


class SiteBoxSelecTS():

    open_popup_search_path = None

    def __init__(self):
        self.name = ''
        self.path = ''
        self.equipment = ''
        self.ok_path = False

    def save_site(self, list_sites, site):
        list_sites.append(site)

    def add_box_info(self):
        box_lay = BoxLayout()
        box_lay.size_hint_y = None
        box_lay.height = 30

        self.box_check_remove = BoxLayout()
        self.box_check_remove.size_hint_x = None
        self.box_check_remove.width = 0

        self.check_remove = CheckBox()
        self.box_check_remove.add_widget(self.check_remove)


        self.tin_site = TextInput(text=self.name)
        self.tin_site.size_hint_x = None
        self.tin_site.width = 130
        self.tin_site.multiline = False

        self.tin_equipment = TextInput()
        self.tin_equipment.text = self.equipment
        self.tin_equipment.size_hint_x = None
        self.tin_equipment.width = 80
        self.tin_equipment.multiline = False

        self.tin_path = TextInput()
        self.tin_path.multiline = False


        self.bt_search = ButtonBlack()
        self.bt_search.text = '...'
        self.bt_search.size_hint_x = None
        self.bt_search.width = 30
        self.bt_search.on_press = self.open_popup_search_path

        box_lay.add_widget(self.box_check_remove)
        box_lay.add_widget(self.tin_site)
        box_lay.add_widget(self.tin_equipment)
        box_lay.add_widget(self.tin_path)
        box_lay.add_widget(self.bt_search)
        box_lay.add_widget(Label(size_hint_x=None, width=3))

        return box_lay

    def open_pop_search_path(self):

        self.popup_search_path = Popup()
        self.windows_search_path = SelecSite(select=self.select_path_ts_files, cancel=self.cancel_path_ts_files)
        self.popup_search_path.content = self.windows_search_path
        self.popup_search_path.title = lang['Select_the_path_containing_the_TS_files'] + '                       ' + self.name

        arq_last_path = open(user + '/.PampaMT/file/last_path_TS', 'r')
        last_path = arq_last_path.readline()
        arq_last_path.close()
        self.windows_search_path.ids.dir.path = last_path

        self.popup_search_path.title_size = 17
        self.popup_search_path.open()

    def select_path_ts_files(self, path_ts_files):
        self.tin_path.text = path_ts_files
        arq_last_path = open(user + '/.PampaMT/file/last_path_TS', 'w')
        arq_last_path.write(path_ts_files)
        arq_last_path.close()
        self.path = self.tin_path.text
        self.popup_search_path.dismiss()

    def cancel_path_ts_files(self):
        self.popup_search_path.dismiss()


class SelecSitePath(BoxLayout):

    # Lang
    bt_add_site = lang['Add_Site']
    bt_remove_site = lang['Remove_Site']
    bt_automatically = lang['Automatically']
    bt_help = lang['Help']
    bt_next = lang['Next']
    bt_cancel = lang['Cancel']
    lb_select_the_sites = lang['Select_the_sites']
    lb_site = lang['Site']
    lb_equipment = lang['Equipment']
    lb_path = lang['Path']



    # Function
    next = ObjectProperty(None)
    cancel = ObjectProperty(None)

    list_sites = []


    def __init__(self, **kwargs):
        super(SelecSitePath, self).__init__(**kwargs)

        self.box_lay_scroll = BoxLayout()
        self.box_lay_scroll.orientation = 'vertical'
        self.box_lay_scroll.size_hint_y = None
        self.box_lay_scroll.bind(minimum_height=self.box_lay_scroll.setter('height'))

        self.scroll_view = ScrollView()

        self.scroll_view.add_widget(self.box_lay_scroll)
        self.ids.lay_box_sites.add_widget(self.scroll_view)

        self.popup_new_site = Popup()
        self.popup_new_site.title = lang['New_Site']
        self.popup_new_site.size_hint = None, None
        self.popup_new_site.size = 300, 160
        self.popup_new_site.title_size = 16
        self.popup_new_site.content = PopupNewSite(make_new_site=self.add_site)

    def open_pop_new_site(self):
        self.popup_new_site.open()

    def add_site(self, site):
        self.popup_new_site.dismiss()

        new_site = SiteBoxSelecTS()
        new_site.name = site
        new_site.open_popup_search_path = new_site.open_pop_search_path

        lis_check_equipments = [self.popup_new_site.content.ids.check_ADU06,
                               self.popup_new_site.content.ids.check_ADU07,
                               self.popup_new_site.content.ids.check_Lims]

        if lis_check_equipments[0].active == True:
            new_site.equipment = 'ADU06'

        elif lis_check_equipments[1].active == True:
            new_site.equipment = 'ADU07'

        elif lis_check_equipments[2].active == True:
            new_site.equipment = 'Lims'

        box_site = new_site.add_box_info()
        box_site.id = site
        self.ids[site] = box_site

        self.box_lay_scroll.add_widget(box_site)
        new_site.save_site(self.list_sites, new_site)


    key_check = True
    def remove_site(self):
        print(self.list_sites)
        self.ids.bt_remove_site.text = lang['Finish_Remove']
        for site in self.list_sites:
            site.box_check_remove.width = 25

        self.key_check_new = self.key_check
        self.key_check = False

        if self.key_check_new == self.key_check:
            self.finish_remove()
            self.key_check = True
        self.key_check_new = False

    def finish_remove(self):

        for site in self.list_sites:
            if site.check_remove.active == True:

                print(site.name)
                self.box_lay_scroll.remove_widget(self.ids[site.name])
                self.list_sites.remove(site)

        for site in self.list_sites:
            site.box_check_remove.width = 0

        for i in self.list_sites:
            print(i.name)
        self.ids.bt_remove_site.text = lang['Remove_Site']

    def auto_fill(self):
        self.popup_auto_fill_site = Popup()
        self.window_popup_auto_fill_site = SelectAutoFillSites(open_search_path_all_site=self.open_pop_search_auto_fill_site)
        self.window_popup_auto_fill_site.cancel = self.cancel_pop_search_auto_fill_site
        self.window_popup_auto_fill_site.auto_fill = self.auto_fill_box_scroll
        self.popup_auto_fill_site.content = self.window_popup_auto_fill_site
        self.popup_auto_fill_site.size_hint = None, None
        self.popup_auto_fill_site.size= 450, 350
        self.popup_auto_fill_site.title = lang['Automatic_Site_Selection']
        self.popup_auto_fill_site.title_size = 17
        self.popup_auto_fill_site.open()

    def cancel_pop_search_auto_fill_site(self):
        self.popup_auto_fill_site.dismiss()

    # Press ... in Auto Fill
    def open_pop_search_auto_fill_site(self):
        self.popup_search_path_auto_fill = Popup()
        self.window_pop_path_auto_fill = SelecSite()
        self.window_pop_path_auto_fill.cancel = self.cancel_pop_path_site_auto_fill_site
        self.window_pop_path_auto_fill.select = self.selec_path_site_auto_fill
        self.popup_search_path_auto_fill.title_size = 17
        self.popup_search_path_auto_fill.title = lang['Select_Directory_with_all_Sites']
        self.popup_search_path_auto_fill.content = self.window_pop_path_auto_fill
        self.popup_search_path_auto_fill.open()

    def cancel_pop_path_site_auto_fill_site(self):
        self.popup_search_path_auto_fill.dismiss()

    def selec_path_site_auto_fill(self, path_all_sites):
        print('select path')
        print(path_all_sites)
        self.window_popup_auto_fill_site.ids.tex_inp_path_all_sites.text = path_all_sites
        self.window_popup_auto_fill_site.ids.lb_path_all_site.text = os.path.basename(path_all_sites) + '/site/'
        self.popup_search_path_auto_fill.dismiss()

    # Press OK in Auto Fill
    def auto_fill_box_scroll(self):
        path_all_site = self.window_popup_auto_fill_site.ids.tex_inp_path_all_sites.text
        structure = self.window_popup_auto_fill_site.ids.tex_inp_structure_site.text

        lis_check_equipments = [self.window_popup_auto_fill_site.ids.check_ADU06,
                                self.window_popup_auto_fill_site.ids.check_ADU07,
                                self.window_popup_auto_fill_site.ids.check_Lims]

        if lis_check_equipments[0].active == True:
            equipment = 'ADU06'

        elif lis_check_equipments[2].active == True:
            equipment = 'Lims'

        elif lis_check_equipments[1].active == True:
            equipment = 'ADU07'

        list_path_site = glob.glob(path_all_site + '/*')
        list_path_site = sorted(list_path_site)

        for path_site in list_path_site:
            if os.path.isdir(path_site):
                new_site = SiteBoxSelecTS()
                new_site.name = os.path.basename(path_site)
                new_site.equipment = equipment
                new_site.path = path_site + '/' + structure


                box_site = new_site.add_box_info()
                new_site.tin_path.text = path_site + '/' + structure
                box_site.id = new_site.name
                self.ids[new_site.name] = box_site

                self.box_lay_scroll.add_widget(box_site)
                new_site.save_site(self.list_sites, new_site)
        self.popup_auto_fill_site.dismiss()


    def help(self):
        pass


class PopupNewDir(BoxLayout):
    make_new_dir = ObjectProperty(None)

    text_tinp = lang['New_Folder']


class ScreenOpenProject(BoxLayout):
    lb_select_project = lang['Select_Project']
    bt_cancel = lang['Cancel']
    bt_select = lang['Select']

    cancel = ObjectProperty(None)
    select = ObjectProperty(None)

# Screen welcome
class Screen(FloatLayout):

    # setting Layouts
    lay_center_bt = BoxLayout()
    lay_center_bt.pos_hint = {'center_x': .77, 'center_y': 1.}

    lay_center = FloatLayout()

    lay_last_project = FloatLayout()
    lay_last_project.size_hint = None, None
    lay_last_project.height = 30
    lay_last_project.width = 150


    # Reading the latest project
    arq_last_project = open(user + '/.PampaMT/file/file_project', 'r')
    last_project = arq_last_project.readline()
    arq_last_project.close()


    lb_last_project = Label(text=lang['Latest_project'])
    lb_last_project.pos = 25, 320
    lb_last_project.size_hint = None, None
    lb_last_project.height = 30
    lb_last_project.width = 120
    lay_last_project.add_widget(lb_last_project)



    # bt_last_project = Button(text=last_project)
    # bt_last_project.size_hint = None, None
    # bt_last_project.height = 20
    # bt_last_project.width = 300
    # bt_last_project.background_color = 0, 0, 0, .5
    # bt_last_project.border = 0, 0, 0, .2
    # bt_last_project.pos = 20, 300
    #
    #
    # lay_last_project.add_widget(bt_last_project)

    list_sites = []
    path_new_project = ''

    def new_project(self):

        self.open_project_key = False
        self.lay_center.clear_widgets()
        self.clear_widgets()
        screen_save_file = FileSave(new_dir=self.open_popup_new_dir,
                                    cancel=self.back_to,
                                    save_new_project=self.save_new_project,
                                    back_to=self.back_to)

        self.lay_center.add_widget(screen_save_file)
        self.add_widget(self.lay_center)


    def open_popup_new_dir(self,path):
        poupup = Popup(content=PopupNewDir(make_new_dir=self.make_new_dir))
        poupup.title = lang['New_Folder']
        poupup.title_size = 16
        poupup.size_hint = None, None
        poupup.height = 120
        poupup.width = 250
        poupup.id = 'pop_new_dir'
        self.ids['pop_new_dir'] = poupup
        global path_new_dir
        self.path_new_dir = path
        poupup.open()

    def make_new_dir(self, name_folder):

        print(self.path_new_dir)
        print(name_folder)
        os.mkdir(self.path_new_dir + '/' + name_folder)

        self.ids['pop_new_dir'].dismiss()


    def open_project(self):
        self.open_project_key = True
        self.clear_widgets()
        self.screen_open_project = ScreenOpenProject(cancel=self.back_to,
                                                     select=self.select_project)
        self.add_widget(self.screen_open_project)

        print('Open project')

    def select_project(self, file_ppmt):
        self.project = read_ppmt_file(file_ppmt[0])
        self.list_sites = self.project.sites

        # !!!!!!!!!!!!!!!!!!!! continuar kkkkkk
        # adicionar para valores intermediarios, se não ter tempo !!!!!!!!!!!!!!!!!!

        arq_file_exec_main = open(user + '/.PampaMT/file/file_exec_main', 'w')
        arq_file_exec_main.write(file_ppmt[0])
        arq_file_exec_main.close()

        arq_file_project = open(user + '/.PampaMT/file/file_project', 'w')
        arq_file_project.write(self.project.name)
        arq_file_project.close()

        self.open_pampamt()


    def open_pampamt(self):

        window.get_running_app().stop()
        Window.close()

        os.chdir(user + '/.PampaMT')
        os.system('./PampaMT.py')


    def close(self):
        pass

    def cancel(self):
        pass

    def save_new_project(self, path, project):

        self.project = ProjectPPMT()
        self.project.name = project



        #self.project = project
        self.path_new_project = path + '/' + project

        if os.path.isdir(user + '/PampaMT/PROC_MT/' + project):
            print('Project already exists in PROC_MT')
            self.open_popop_project_already_exists(project, 'PROC_MT')
            print(' ')
        elif os.path.isdir(user + '/PampaMT/DADOS_MT/' + project):
            print('Project already exists in DADOS_MT')
            self.open_popop_project_already_exists(project, 'DADOS_MT')
            print(' ')
        else:
            print('Created /PampaMT/PROC_MT/' + project)
            os.mkdir(user + '/PampaMT/PROC_MT/' + project)

            print('Created /PampaMT/DADOS_MT/' + project)
            os.mkdir(user + '/PampaMT/DADOS_MT/' + project)

            copy_model = (user + '/PampaMT/modelo/*')
            paste_model = (user + '/PampaMT/PROC_MT/' + project + '/')

            print('Copying Modelo to /PampaMT/PROC_MT/' + project)
            os.system('cp -r ' + copy_model + ' ' + paste_model)
            print(' ')

            if os.path.isdir(self.path_new_project):
                self.open_popup_dir_already_exists(project)
                print('Project already: ' + self.path_new_project)
                print(' ')
            else:

                os.mkdir(self.path_new_project)
                print('Created Project in ' + self.path_new_project)

                self.project.path_file_ppmt = self.path_new_project + '/' + project + '.' + 'ppmt'
                #self.project.save()
                save(self.project)

                # arq_ppmt = open(self.path_new_project + '/' + project + '.' + 'ppmt', 'w')
                # arq_ppmt.close()
                print('Created the file .ppmt in ' + self.path_new_project)


                path_arq_ppmt = self.path_new_project + '/' + project + '.' + 'ppmt'
                file_exec_main = open(user + '/.PampaMT/file/file_exec_main', 'w')
                file_exec_main.write(path_arq_ppmt)
                file_exec_main.close()
                print("Written PATH's file .ppmt in /.PampaMT/file/file_exec_main")


                file_project = open(user + '/.PampaMT/file/file_project', 'w')
                file_project.write(project)
                file_project.close()
                print("Written name project in /.PampaMT/file/file_project")
                print(' ')

                self.sel_site_path()

    def sel_site_path(self):
        self.clear_widgets()
        self.window_selec_site = SelecSitePath(next=self.open_popup_copy_sites, cancel=self.back_to_and_remove)

        self.add_widget(self.window_selec_site)
        #self.add_widget(SelecSitePath())

    def open_popup_copy_sites(self):

        if self.open_project_key == True:
            pass
        else:
            for site in self.window_selec_site.list_sites:
                save_site = Site()
                save_site.name = site.name
                save_site.equipment = site.equipment
                save_site.path_origin = site.path
                save_site.project = self.project.name

                self.list_sites.append(save_site)



        num_sites = len(self.list_sites)
        title_pop = lang['Copying']
        lang_seconds = lang['seconds']
        lang_minutes = lang['minutes']
        lang_cancel = lang['Cancel']

        self.popup_copy_site = PopUpLoading(title_pop=title_pop, lang_seconds=lang_seconds,
                                            lang_minutes=lang_minutes, lang_cancel=lang_cancel, cancel=self.cancel_copy)
        self.popup_copy_site.num_max = num_sites


        self.popup_copy_site.open()

        self.popup_copy_site.papallel_start(self.copy_sites)

    def cancel_copy(self):

        self.break_copy = True

    def copy_sites(self):
        self.break_copy = False
        number_site = 1
        for site in self.list_sites:

            time_go = timer()
            path_site_origin = site.path_origin + '/*'
            path_data_mt = user + '/PampaMT/DADOS_MT/' + self.project.name + '/' + site.name + '/'
            path_mkdir = user + '/PampaMT/DADOS_MT/' + self.project.name + '/' + site.name

            if (self.break_copy == False) and (site.copy == False):
                os.mkdir(path_mkdir)
                os.system('cp -r ' + path_site_origin + ' ' + path_data_mt)
                site.copy = True

                self.project.sites = self.list_sites
                save(self.project)
                #self.project.save()


            else:
                self.popup_copy_site.title = lang['Canceling']
                os.system('rm -r ' + user + '/PampaMT/DADOS_MT/' + self.project.name + '/*')
                self.popup_copy_site.dismiss()
                break

            self.popup_copy_site.count_time = number_site
            time_end = timer()
            self.popup_copy_site.time_one_step = time_end - time_go
            number_site += 1
            self.popup_copy_site.title = self.popup_copy_site.title_pop + '      ' + site.name

        if self.break_copy == False:
            self.popup_copy_site.dismiss()
            self.open_pop_convert_bin_asc()

    def open_pop_convert_bin_asc(self):

        self.pop_convert_bin_asc = Popup()
        self.window_convert_bin_asc = PopupConvertBinAsc(bt_ok=self.open_popup_convert_sites, cancel=self.cancel_pop_convert_bin_asc)
        self.pop_convert_bin_asc.content = self.window_convert_bin_asc
        self.pop_convert_bin_asc.title = lang['Convert_bin_format_to_asc']
        self.pop_convert_bin_asc.title_size = 17
        self.pop_convert_bin_asc.size_hint = None, None
        self.pop_convert_bin_asc.size = 300, 100
        self.pop_convert_bin_asc.open()

    def cancel_pop_convert_bin_asc(self):
        self.pop_convert_bin_asc.dismiss()

    def open_popup_convert_sites(self):
        self.pop_convert_bin_asc.dismiss()

        num_sites = len(self.list_sites)
        title_pop = lang['Converting']
        lang_seconds = lang['seconds']
        lang_minutes = lang['minutes']
        lang_cancel = lang['Cancel']

        self.popup_convert_site = PopUpLoading(title_pop=title_pop, lang_seconds=lang_seconds,
                                            lang_minutes=lang_minutes, lang_cancel=lang_cancel, cancel=self.cancel_convert)
        self.popup_convert_site.num_max = num_sites
        self.popup_convert_site.open()

        self.popup_convert_site.papallel_start(self.convert_bin_asc)

    def cancel_convert(self):

        # Cancel conversion of files TS

        self.break_convert = True

    def convert_bin_asc(self):

        self.break_convert = False
        os.chdir(user + '/PampaMT/PROC_MT/' + self.project.name)
        print('Mudou o diretorio')
        print(user + '/PampaMT/PROC_MT/' + self.project.name)
        number_site = 1
        for site in self.list_sites:

            time_go = timer()

            if (self.break_convert == False) and (site.ats2asc == False):


                os.system('ats2asc --site-name ' + site.name + ' ../../DADOS_MT/'+ self.project.name + '/' + site.name + '/')
                site.ats2asc = True
                print('Convertendo ... ats2asc --site-name ' + site.name + ' ../../DADOS_MT/' + site.name)
                site.ats2asc = True

                site.coordinates = read_ats_coordinates('../../DADOS_MT/' + site.project + '/' + site.name)
                print(lang['Saving_Coordinates'] + site.name)

                self.project.sites = self.list_sites
                #self.project.save()
                save(self.project)
            else:
                self.popup_convert_site.title = lang['Canceling']
                #os.system('rm -r ' + user + '/PampaMT/DADOS_MT/' + self.project.name + '/*')
                print('Cancelar Convert')
                self.popup_copy_site.dismiss()
                break

            self.popup_convert_site.count_time = number_site
            time_end = timer()
            self.popup_convert_site.time_one_step = time_end - time_go
            number_site += 1
            self.popup_convert_site.title = self.popup_convert_site.title_pop + '      ' + site.name

        if self.break_copy == False:
            self.popup_convert_site.dismiss()
            self.processamentoZ()

    def open_popop_project_already_exists(self, project, proc_or_dados):

        # Creates and opens Popup: Project already exists

        text_popup = lang['The_project'] + ': ' + project + '\n ' + lang['already_exists_in'] + ' ' + proc_or_dados
        popup = PopupPampaMT(text_popup=text_popup, title=lang['Already_Exists'])
        popup.size_hint = None, None
        popup.height = 100
        popup.width = 250
        popup.title_size = 16
        popup.open()

    def open_popup_dir_already_exists(self, project):

        # Creates and opens Popup: create a new directory

        text_popup = lang['The_project'] + ': ' + project + '\n ' + lang['already_exists']
        popup = PopupPampaMT(text_popup=text_popup, title=lang['Already_Exists'])
        popup.size_hint = None, None
        popup.height = 100
        popup.width = 200
        popup.title_size = 16
        popup.open()

    def open_ppmt(self):
        pass

    def back_to_and_remove(self):

        # Function to remove the files creates in PROC_MT, DADOS_MT and Path_New_Project
        # Restores the home screen
        # Clear the list_site

        os.system('rm -r ' + user + '/PampaMT/PROC_MT/' + self.project.name)
        print('Removing: ' + user + '/PampaMT/PROC_MT/' + self.project.name)

        os.system('rm -r ' + user + '/PampaMT/DADOS_MT/' + self.project.name)
        print('Removing: '+ user + '/PampaMT/DADOS_MT/' + self.project.name)

        os.system('rm -r ' + self.path_new_project)
        print('Removing: ' + self.path_new_project)

        self.back_to()
        self.list_sites = []

    def back_to(self):

        # Restores the home screen


        self.lay_center.clear_widgets()
        self.clear_widgets()
        self.lay_center_bt.clear_widgets()
        image_back_ground = Image()
        image_back_ground.source = 'image/background_ppmt_main.png'
        button_new_open_close = ButtonNewOpen(new_proj=self.new_project, open_proj=self.open_project)
        self.add_widget(image_back_ground)
        self.lay_center_bt.add_widget(button_new_open_close)
        self.lay_center.add_widget(self.lay_center_bt)
        self.lay_center.add_widget(self.lay_last_project)
        self.add_widget(self.lay_center)

    def processamentoZ(self):

        self.clear_widgets()
        print('processamentoZ')


        self.bt_test_processingZ = ButtonBlack()
        self.bt_test_processingZ.text = lang['ProcessingZ']
        self.bt_test_processingZ.center_y = 250
        self.bt_test_processingZ.center_x = 400
        self.bt_test_processingZ.on_press = self.open_screen_processingZ
        self.add_widget(self.bt_test_processingZ)

    def open_screen_processingZ(self):
        self.clear_widgets()
        size_accordion = (len(self.list_sites) * 22) + 215
        screen = ProcessingZ(self.list_sites, self.project, lang=lang, size_accordeon_scroll=size_accordion,
                             openPampaMT=self.openPampaMT)
        self.add_widget(screen)

    def finish_project(self):

        list_site = self.project.sites

        unit_progress_bar = int(100/len(list_site))

        print(unit_progress_bar)
        for site in list_site:

            # site.coordinates = read_ats_coordinates('../../DADOS_MT/' + site.project + '/' + site.name)
            # print(lang['Saving_Coordinates'] + site.name)
            self.lb_finish.text = lang['Saving_Coordinates'] + site.name
            #time.sleep(0.8)

            site.files_zss, site.files_plot = self.search_zss_file(site)
            self.progress_bar_finish.value += unit_progress_bar

        self.lb_finish.text = 'Finish    Opening PampaMT... '


        self.open_pampamt()

    def search_zss_file(self, site):

        files_plot = {}
        files_zss = {}

        if site.equipment == 'ADU06':
            for band in ['A', 'B', 'F', 'C', 'D']:
                list_zss_file_band = glob.glob('MT*/' + site.name + '*' + band + '*.zss')
                list_zss_file_band = sorted(list_zss_file_band)
                files_zss['band_' + band] = list_zss_file_band

                list_file_plot = []
                for file_zss in list_zss_file_band:
                    print(file_zss)
                    file_plot = make_file_pplt(file_zss, site.name, band)
                    self.lb_finish.text = lang['Creating:'] + file_plot.name.replace('zss', 'pplt') + '   ' + file_plot.rate
                    save_file_pplt(file_plot)
                    list_file_plot.append(file_plot)
                files_plot['band_' + band] = list_file_plot
            print(files_zss, files_plot)
            return files_zss, files_plot

        elif site.equipment == 'ADU07':
            for band in ['65536H', '4096H', '128H', '4H']:
                list_zss_file_band = glob.glob('MT*/' + site.name + '*' + band + '*.zss')
                list_zss_file_band = sorted(list_zss_file_band)
                files_zss['band_' + band] = list_zss_file_band

                list_file_plot = []
                for file_zss in list_zss_file_band:
                    print(file_zss)
                    file_plot = make_file_pplt(file_zss, site.name, band)
                    self.lb_finish.text = lang['Creating:'] + file_plot.name.replace('zss', 'pplt') + '   ' + file_plot.rate
                    save_file_pplt(file_plot)
                    list_file_plot.append(file_plot)
                files_plot['band_' + band] = list_file_plot
            print(files_zss, files_plot)
            return files_zss, files_plot

    def openPampaMT(self, project):
        
        self.clear_widgets()

        self.add_widget(self.image_back_ground)
        self.project = project

        lb_creating_the_project = Label()
        lb_creating_the_project.text = lang['Creating_the_Project']
        lb_creating_the_project.bold = True
        lb_creating_the_project.font_size = 17

        lb_creating_the_project.size_hint = None, None
        lb_creating_the_project.height = 30
        lb_creating_the_project.width = 150

        lb_creating_the_project.center_y = 250
        lb_creating_the_project.center_x = 400

        self.add_widget(lb_creating_the_project)

        self.progress_bar_finish = ProgressBar()
        self.progress_bar_finish.size_hint = None, None
        self.progress_bar_finish.width = 350
        self.progress_bar_finish.height = 10
        self.progress_bar_finish.value = 1
        self.progress_bar_finish.center_x = 400
        self.progress_bar_finish.center_y = 150
        self.add_widget(self.progress_bar_finish)

        self.lb_finish = Label(text=lang['Creating...'])
        self.lb_finish.size_hint = None, None
        self.lb_finish.width = 350
        self.lb_finish.height = 30
        self.lb_finish.center_x = 400
        self.lb_finish.center_y = 120
        self.add_widget(self.lb_finish)

        parallel_progress_bar = threading.Thread(target=self.finish_project)
        parallel_progress_bar.start()



    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        self.bt_last_project = Button(text=self.last_project)
        self.bt_last_project.size_hint = None, None
        self.bt_last_project.height = 20
        self.bt_last_project.width = 300
        self.bt_last_project.background_color = 0, 0, 0, .5
        self.bt_last_project.border = 0, 0, 0, .2
        self.bt_last_project.pos = 20, 300
        self.bt_last_project.on_press = self.open_pampamt

        self.lay_last_project.add_widget(self.bt_last_project)


        # Background Image
        self.image_back_ground = Image()
        self.image_back_ground.source = 'image/background_ppmt_main.png'
        button_new_open_close = ButtonNewOpen(new_proj=self.new_project, open_proj=self.open_project)

        self.add_widget(self.image_back_ground)
        self.lay_center_bt.add_widget(button_new_open_close)
        self.lay_center.add_widget(self.lay_center_bt)


        self.lay_center.add_widget(self.lay_last_project)
        self.add_widget(self.lay_center)



        # teste
        #self.openPampaMT(ProjectTeste())







# Class build App
class DiagMain(App):
    def build(self):
        return Screen()


window = DiagMain()
window.icon = user + '/.PampaMT/image/icon.png'
window.title = lang['Welcome_to_PampaMT']
Window.size = 800, 500


if __name__ == '__main__':
    print('Start PampaMT')
    window.run()
