#!/usr/bin/python3
#coding: utf-8

__author__ = 'Patrick Rogger Garcia'
__email__ = 'patrick_rogger@hotmail.com'
__version__ = '0.0.1'
__status__ = 'Production'

# App for read dic binary

# Packages import
import pickle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class Screen(BoxLayout):
    i = 0
    path_file = ''
    def add(self):

        box_keys_trad = BoxLayout(size_hint_y=None, height=30)
        tex_in_key = TextInput()
        tex_in_key.multiline = False
        tex_in_key.id = 'text_key_' + str(self.i)
        self.ids['text_key_' + str(self.i)] = tex_in_key

        tex_in_trad = TextInput()
        tex_in_trad.multiline = False
        tex_in_trad.id = 'text_trad_' + str(self.i)
        self.ids['text_trad_' + str(self.i)] = tex_in_trad

        box_keys_trad.add_widget(tex_in_key)
        box_keys_trad.add_widget(tex_in_trad)
        self.ids.box_keys.add_widget(box_keys_trad)
        self.i += 1

    def save(self):
        dic_lang_save = {}
        for i in range(self.i):
            key = self.ids['text_key_' + str(i)].text
            trad = self.ids['text_trad_' + str(i)].text
            dic_lang_save[key] = trad

        arq_save = open(self.path_file, 'wb')
        pickle.dump(dic_lang_save,arq_save)


    def open(self, selection):
        path = "".join(selection)

        self.path_file = path
        arq_dic = open(path, 'rb')
        dic_lang_load = pickle.load(arq_dic)
        arq_dic.close()

        list_keys = dic_lang_load.keys()

        box_keys = BoxLayout(orientation='vertical')
        box_keys.size_hint_y = None
        box_keys.bind(minimum_height=box_keys.setter('height'))
        box_keys.id = 'box_keys'
        self.ids['box_keys'] = box_keys

        scroll = ScrollView()

        global i
        for key in list_keys:

            box_keys_trad = BoxLayout(size_hint_y=None, height=30)
            trad = dic_lang_load[key]

            tex_in_key = TextInput(text=str(key))
            tex_in_key.multiline = False
            tex_in_key.id = 'text_key_' + str(self.i)
            self.ids['text_key_' + str(self.i)] = tex_in_key

            tex_in_trad = TextInput(text=str(trad))
            tex_in_trad.multiline = False
            tex_in_trad.id = 'text_trad_' + str(self.i)
            self.ids['text_trad_' + str(self.i)] = tex_in_trad

            box_keys_trad.add_widget(tex_in_key)
            box_keys_trad.add_widget(tex_in_trad)

            box_keys.add_widget(box_keys_trad)
            self.i += 1

        scroll.add_widget(box_keys)
        self.ids.screen_dic.add_widget(scroll)

class WindowMain(App):
    def build(self):
        return Screen()

window = WindowMain()
window.title = 'Dictionary Reader'

window.run()


