
from math import log10
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.lang import Builder

import pickle

kivy_code = '''
<LabelRot@Label>
    canvas.before:
        PushMatrix
        Rotate:
            angle: 90
            origin: self.center
    canvas.after:
        PopMatrix
'''
Builder.load_string(kivy_code)
class LabelRot(Label):
    pass

def coorlog_to_pixel(coor, v0, fzoom, exp_min):

    x = int(v0 + ((log10(coor) + exp_min) * fzoom))
    return x

def draws_lines_rho( x0, y0, dx, dy, fzoom, border, xmin, xmax, ymin, ymax, limx, limy, label_y):
    xf = x0 + dx
    yf = y0 + dy

    deca_x = range(xmin, xmax + 1)
    deca_y = range(ymin, ymax + 1)

    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9,
             10, 20, 30, 40, 50, 60, 70, 80, 90,
             100, 200, 300, 400, 500, 600, 700, 800, 900,
             1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
             10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000,
             100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000,
             1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000,
             10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000,
             100000000]

    scale_log = []
    for i in scale:
        scale_log.append(log10(i))

    scale_log_zoom = []
    for i in scale_log:
        scale_log_zoom.append(i * fzoom)

    lay = FloatLayout()
    with lay.canvas:
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, y0, xf, y0], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, y0, x0, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[xf, y0, xf, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, yf, xf, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Color(rgba=[.2, .2, .2, 1.])
        Ellipse(size=[6, 6], pos=[int(((dx / 3) * 2) + x0 - 23), yf + 7])

        c = 0
        for i in scale_log_zoom:
            if scale[c] > limx:
                continue
            else:
                Color(rgba=[0., 0., 0., 1.])
                Line(points=[i + x0, y0, i + x0, y0 - 5])
                c += 1
        c = 0
        for i in scale_log_zoom:
            if scale[c] > limy:
                continue
            else:
                Color(rgba=[0, 0, 0, 1])
                Line(points=[x0, i + y0, x0 - 5, i + y0])
            c += 1

        c = 0
        for i in scale_log_zoom:
            if scale[c] > limy:
                continue
            else:
                Color(rgba=[0, 0, 0, 1])
                Line(points=[xf, i + y0, xf + 5, i + y0])
            c += 1

        for i in deca_y:

            if deca_y[0] < 0:
                pos = -deca_y[0]

            lb = Label()
            lb.color = [0, 0, 0, 1]
            lb.markup = True
            lb.text = '10' + '[sup][size=10]' + str(i) + '[/size][/sup]'
            lb.size_hint = None, None
            lb.height = 30
            lb.width = 30

            y = int((y0 - 20) + ((i + pos) * fzoom))
            lb.pos = x0 - 35, y
            lay.add_widget(lb)

        for i in deca_x:

            if deca_x[0] < 0:
                pos = -deca_x[0]

            lb = Label()
            lb.color = [0, 0, 0, 1]
            lb.markup = True
            lb.text = '10' + '[sup][size=10]' + str(i) + '[/size][/sup]'
            lb.size_hint = None, None
            lb.height = 30
            lb.width = 30

            x = int((x0 - 20) + ((i + pos) * fzoom))
            lb.pos = x + 5, y0 - 35
            lay.add_widget(lb)

    if label_y == True:
        lb_rho_ohm_meter = LabelRot()
        lb_rho_ohm_meter.size_hint = None, None
        lb_rho_ohm_meter.height = 100
        lb_rho_ohm_meter.width = 25
        lb_rho_ohm_meter.markup = True
        lb_rho_ohm_meter.italic = True
        lb_rho_ohm_meter.text = 'ρ (Ω.m)'
        lb_rho_ohm_meter.color = [0., 0., 0., 1.]
        lb_rho_ohm_meter.center_x = x0 - 40
        lb_rho_ohm_meter.center_y = int(y0 + dy / 2)

        lay.add_widget(lb_rho_ohm_meter)

    bt_rho_xy = PointPlotEX()
    bt_rho_xy.center_x = int(((dx/3) + x0)-20)
    bt_rho_xy.center_y = yf + 10
    lb_rho_xy = Label()
    lb_rho_xy.size_hint = None, None
    lb_rho_xy.height = 30
    lb_rho_xy.width = 30
    lb_rho_xy.center_x = int((dx/3) + x0)
    lb_rho_xy.center_y = yf + 15
    lb_rho_xy.markup = True
    lb_rho_xy.text = 'ρ[sub]xy[/sub]'
    lb_rho_xy.color = [.2, .2, .2, 1.]
    lb_rho_xy.font_size = 23

    lay.add_widget(bt_rho_xy)
    lay.add_widget(lb_rho_xy)


    lb_rho_yx = Label()
    lb_rho_yx.size_hint = None, None
    lb_rho_yx.height = 30
    lb_rho_yx.width = 30
    lb_rho_yx.center_x = int(((dx / 3) * 2) + x0)
    lb_rho_yx.center_y = yf + 15
    lb_rho_yx.markup = True
    lb_rho_yx.text = 'ρ[sub]yx[/sub]'
    lb_rho_yx.color = [.2, .2, .2, 1.]
    lb_rho_yx.font_size = 23


    lay.add_widget(lb_rho_yx)

    return lay


def draws_lines_phi(x0, y0, dx, dy, fzoom,fzoomy, border, xmin, xmax, ymin, ymax, limx, limy, label_y, scale_y):
    xf = x0 + dx
    yf = y0 + dy

    deca_x = range(xmin, xmax + 1)
    deca_y = range(ymin, ymax+5, 5)

    if limy == 90:
        lb_y = [0, 45, 90]
    elif limy == 180:
        lb_y = [0, 90, 180]

    #lb_y = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]

    #lb_y = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9,
             10, 20, 30, 40, 50, 60, 70, 80, 90,
             100, 200, 300, 400, 500, 600, 700, 800, 900,
             1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
             10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000,
             100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000,
             1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000,
             10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000,
             100000000]

    scale_log = []
    for i in scale:
        scale_log.append(log10(i))

    scale_log_zoom = []
    for i in scale_log:
        scale_log_zoom.append(i * fzoom)

    lay = FloatLayout()
    with lay.canvas:
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, y0, xf, y0], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, y0, x0, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[xf, y0, xf, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, yf, xf, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Color(rgba=[.2, .2, .2, 1.])
        Ellipse(size=[6, 6], pos=[int(((dx / 3) * 2) + x0 + 5), yf + 10])

        c = 0
        for i in scale_log_zoom:
            if scale[c] > limx:
                continue
            else:
                Color(rgba=[0., 0., 0., 1.])
                Line(points=[i + x0, y0, i + x0, y0 - 5])
                c += 1

        for i in deca_y:
            i = int(i * fzoomy)
            Color(rgba=[0., 0., 0., 1.])
            Line(points=[x0 - 5, i + y0, x0, i + y0])

        for i in deca_y:
            i = int(i * fzoomy)
            Color(rgba=[0., 0., 0., 1.])
            Line(points=[xf + 5, i + y0, xf, i + y0])

        if scale_y == True:
            for i in lb_y:

                lb_phi = Label()
                lb_phi.color = [0, 0, 0, 1]
                lb_phi.markup = True
                lb_phi.text = str(i)
                lb_phi.size_hint = None, None
                lb_phi.height = 30
                lb_phi.width = 30

                if limy == 180:
                    y = (i * fzoomy) + y0

                elif limy == 90:
                    y = ((i/2) * fzoomy) + y0

                lb_phi.center_x = xf + 25
                lb_phi.center_y = y

                lay.add_widget(lb_phi)

        for i in deca_x:

            if deca_x[0] < 0:
                pos = -deca_x[0]

            lb = Label()
            lb.color = [0,0,0,1]
            lb.markup = True
            lb.text = '10' + '[sup][size=10]' + str(i) + '[/size][/sup]'
            lb.size_hint = None, None
            lb.height = 30
            lb.width = 30

            x = int((x0 - 15) + ((i + pos) * fzoom))
            lb.pos = x, y0 - 30
            lay.add_widget(lb)

    if label_y == True:

        lb_rho_ohm_meter = LabelRot()
        lb_rho_ohm_meter.size_hint = None, None
        lb_rho_ohm_meter.height = 100
        lb_rho_ohm_meter.width = 25
        lb_rho_ohm_meter.markup =True
        lb_rho_ohm_meter.italic = True
        lb_rho_ohm_meter.text = 'φ (graus)'
        lb_rho_ohm_meter.color = [0., 0., 0., 1.]
        lb_rho_ohm_meter.center_x = x0 - 20
        lb_rho_ohm_meter.center_y = int(y0 + dy/2)

        lay.add_widget(lb_rho_ohm_meter)

    bt_rho_xy = PointPlotEX()
    bt_rho_xy.center_x = int(((dx / 3) + x0) - 50)
    bt_rho_xy.center_y = yf + 14
    lb_rho_xy = Label()
    lb_rho_xy.size_hint = None, None
    lb_rho_xy.height = 30
    lb_rho_xy.width = 30
    lb_rho_xy.center_x = int((dx / 3) + x0 - 20)
    lb_rho_xy.center_y = yf + 15
    lb_rho_xy.markup = True
    lb_rho_xy.text = 'φ[sub][size=15]xy[/size][/sub]'
    lb_rho_xy.color = [.2, .2, .2, 1.]
    lb_rho_xy.font_size = 17

    lay.add_widget(bt_rho_xy)
    lay.add_widget(lb_rho_xy)


    lb_rho_yx = Label()
    lb_rho_yx.size_hint = None, None
    lb_rho_yx.height = 30
    lb_rho_yx.width = 30
    lb_rho_yx.center_x = int(((dx / 3) * 2) + x0 + 40)
    lb_rho_yx.center_y = yf + 15
    lb_rho_yx.markup = True
    lb_rho_yx.text = 'φ[sub][size=15]yx[/size][/sub]'
    lb_rho_yx.color = [.2, .2, .2, 1.]
    lb_rho_yx.font_size = 17


    lay.add_widget(lb_rho_yx)


    return lay


def draws_lines_Z(x0, y0, dx, dy, fzoom,fzoomy, border, xmin, xmax, ymin, ymax, limx, limy, label_y, scale_y, component):
    xf = x0 + dx
    yf = y0 + dy

    deca_x = range(xmin, xmax + 1)
    deca_y = range(ymin, ymax, 5)

    # if limy == 90:
    #     lb_y = [0, 45, 90]
    # elif limy == 180:
    #     lb_y = [0, 90, 180]

    lb_y = [-15, -10, -5, 0, 5, 10, 15]

    #lb_y = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9,
             10, 20, 30, 40, 50, 60, 70, 80, 90,
             100, 200, 300, 400, 500, 600, 700, 800, 900,
             1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
             10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000,
             100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000,
             1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000,
             10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000,
             100000000]

    scale_log = []
    for i in scale:
        scale_log.append(log10(i))

    scale_log_zoom = []
    for i in scale_log:
        scale_log_zoom.append(i * fzoom)

    lay = FloatLayout()
    with lay.canvas:
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, y0, xf, y0], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, y0, x0, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[xf, y0, xf, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Line(points=[x0, yf, xf, yf], width=border)
        Color(rgba=[0, 0, 0, 1])
        Color(rgba=[.2, .2, .2, 1.])
        Ellipse(size=[6, 6], pos=[int(((dx / 3) * 2) + x0 + 5), yf + 10])

        c = 0
        for i in scale_log_zoom:
            if scale[c] > limx:
                continue
            else:
                Color(rgba=[0., 0., 0., 1.])
                Line(points=[i + x0, y0, i + x0, y0 - 5])
                c += 1

        for i in deca_y:
            i = int(i * fzoomy)
            Color(rgba=[0., 0., 0., 1.])
            Line(points=[x0 - 5, i + y0, x0, i + y0])

        for i in deca_y:
            i = int(i * fzoomy)
            Color(rgba=[0., 0., 0., 1.])
            Line(points=[xf + 5, i + y0, xf, i + y0])

        if scale_y == True:
            for i in lb_y:

                lb_phi = Label()
                lb_phi.color = [0, 0, 0, 1]
                lb_phi.markup = True
                lb_phi.text = str(i)
                lb_phi.size_hint = None, None
                lb_phi.height = 30
                lb_phi.width = 30

                if limy == 180:
                    y = (i/2 * fzoomy) + y0

                elif limy == 90:
                    y = ((i+15) * fzoomy) + y0

                lb_phi.center_x = xf + 25
                lb_phi.center_y = y

                lay.add_widget(lb_phi)

        for i in deca_x:

            if deca_x[0] < 0:
                pos = -deca_x[0]

            lb = Label()
            lb.color = [0,0,0,1]
            lb.markup = True
            lb.text = '10' + '[sup][size=10]' + str(i) + '[/size][/sup]'
            lb.size_hint = None, None
            lb.height = 30
            lb.width = 30

            x = int((x0 - 15) + ((i + pos) * fzoom))
            lb.pos = x, y0 - 30
            lay.add_widget(lb)

    lb_title = Label()
    lb_title.color = [0, 0, 0, 1.]
    lb_title.font_size = 17
    lb_title.text = 'Z' + component
    lb_title.size_hint = None, None
    lb_title.height = 30
    lb_title.width = 370
    lb_title.center_x = int((lb_title.width/2) + x0) - 25
    lb_title.center_y = yf + 15

    #lay.add_widget(lb_title)

    if label_y == True:

        lb_rho_ohm_meter = LabelRot()
        lb_rho_ohm_meter.size_hint = None, None
        lb_rho_ohm_meter.height = 100
        lb_rho_ohm_meter.width = 25
        lb_rho_ohm_meter.markup =True
        lb_rho_ohm_meter.italic = True
        lb_rho_ohm_meter.text = 'φ (graus)'
        lb_rho_ohm_meter.color = [0., 0., 0., 1.]
        lb_rho_ohm_meter.center_x = x0 - 40
        lb_rho_ohm_meter.center_y = int(y0 + dy/2)

        lay.add_widget(lb_rho_ohm_meter)

    bt_rho_xy = PointPlotEX()
    bt_rho_xy.center_x = int(((dx / 3) + x0) - 50)
    bt_rho_xy.center_y = yf + 14
    lb_rho_xy = Label()
    lb_rho_xy.size_hint = None, None
    lb_rho_xy.height = 30
    lb_rho_xy.width = 30
    lb_rho_xy.center_x = int((dx / 3) + x0 - 20)
    lb_rho_xy.center_y = yf + 15
    lb_rho_xy.markup = True
    lb_rho_xy.text = 'Re Z[sub][size=15]'+ component +'[/size][/sub]'
    lb_rho_xy.color = [.2, .2, .2, 1.]
    lb_rho_xy.font_size = 17

    lay.add_widget(bt_rho_xy)
    lay.add_widget(lb_rho_xy)


    lb_rho_yx = Label()
    lb_rho_yx.size_hint = None, None
    lb_rho_yx.height = 30
    lb_rho_yx.width = 30
    lb_rho_yx.center_x = int(((dx / 3) * 2) + x0 + 40)
    lb_rho_yx.center_y = yf + 15
    lb_rho_yx.markup = True
    lb_rho_yx.text = 'Im Z[sub][size=15]'+ component +'[/size][/sub]'
    lb_rho_yx.color = [.2, .2, .2, 1.]
    lb_rho_yx.font_size = 17


    lay.add_widget(lb_rho_yx)


    return lay

class PointPlot(Button):
    cor = []
    cor_no = [0, 0, 0, .2]
    active = False
    active_n = 0
    n = -1

    def __init__(self, file_pplt,i, **kwargs):
        super(PointPlot, self).__init__(**kwargs)
        self.i = i

        self.obj_file = file_pplt
        self.background_normal = ' '
        self.size_hint = None, None
        self.border = [0, 0, 0, 0]
        self.height = 6
        self.width = 6
        self.background_color = self.cor_no
        self.on_press = self.select
        self.points_inte = []

    def select(self):
        self.background_color = self.cor
        self.on_press = self.no_select
        self.active = True
        self.active_n = 1
        print('active: ' + str(self.active))
        self.obj_file.activated[self.i] = True

        arq_file_pplt = open('PampaMT/file_pplt/' + self.obj_file.site + '/' + self.obj_file.rate + '_' + self.obj_file.name_plot, 'wb')
        pickle.dump(self.obj_file, arq_file_pplt)
        arq_file_pplt.close()



    def no_select(self):
        self.background_color = self.cor_no
        self.on_press = self.select
        self.active = False
        self.active_n = 0
        print('active: ' + str(self.active))
        self.obj_file.activated[self.i] = False

        arq_file_pplt = open('PampaMT/file_pplt/' + self.obj_file.site + '/' + self.obj_file.rate + '_' + self.obj_file.name_plot, 'wb')
        pickle.dump(self.obj_file, arq_file_pplt)
        arq_file_pplt.close()


class PointPlotCirc(Button):
    cor = []
    cor_no = [0, 0, 0, .2]
    active = False
    active_n = 0
    n = -1

    def __init__(self, file_pplt,i, **kwargs):
        super(PointPlotCirc, self).__init__(**kwargs)
        self.i = i

        self.obj_file = file_pplt
        self.background_normal = ' '
        self.size_hint = None, None
        self.border = [0, 0, 0, 0]
        self.height = 6
        self.width = 6
        #self.background_color = self.cor_no

        self.canvas.clear()

        with self.canvas.before:
            Color(rgba=self.cor_no)
            Ellipse(size=self.size, pos=self.pos)


        self.on_press = self.select
        self.points_inte = []

    def select(self):

        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=self.size, pos=self.pos)

        #self.background_color = self.cor
        self.on_press = self.no_select
        self.active = True
        self.active_n = 1
        print('active: ' + str(self.active))
        self.obj_file.activated[self.i] = True

        arq_file_pplt = open('PampaMT/file_pplt/' + self.obj_file.site + '/' + self.obj_file.rate + '_' + self.obj_file.name_plot, 'wb')
        pickle.dump(self.obj_file, arq_file_pplt)
        arq_file_pplt.close()



    def no_select(self):
        #self.background_color = self.cor_no

        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor_no)
            Ellipse(size=self.size, pos=self.pos)

        self.on_press = self.select
        self.active = False
        self.active_n = 0
        print('active: ' + str(self.active))
        self.obj_file.activated[self.i] = False

        arq_file_pplt = open('PampaMT/file_pplt/' + self.obj_file.site + '/' + self.obj_file.rate + '_' + self.obj_file.name_plot, 'wb')
        pickle.dump(self.obj_file, arq_file_pplt)
        arq_file_pplt.close()

class PointPlotEX(Button):
    cor_no = [.2, .2, .2, 1.]

    def __init__(self, **kwargs):
        super(PointPlotEX, self).__init__(**kwargs)

        self.background_normal = ' '
        self.size_hint = None, None
        self.border = [0, 0, 0, 0]
        self.height = 6
        self.width = 6
        self.background_color = self.cor_no



class PointPlotCircEX(Button):
    cor_no = [0, 0, 0, 1.]

    def __init__(self, **kwargs):
        super(PointPlotCircEX, self).__init__(**kwargs)

        self.background_normal = ' '
        self.size_hint = None, None
        self.border = [0, 0, 0, 0]
        self.height = 6
        self.width = 6

        self.canvas.clear()
        self.canvas.before.clear()

        with self.canvas.before:
            Color(rgba=self.cor_no)
            Ellipse(size=self.size, pos=self.pos)