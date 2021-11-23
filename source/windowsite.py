import os
import subprocess
import pickle
# os.chdir('/home/patrick/PampaMT/PROC_MT/zTest')


class FilePPLT():
    def __init__(self):

        self.name = ''
        self.name_plot = ''
        self.site = ''
        self.band = ''

        self.active_file = False

        self.rate = ''

        self.color = []

        self.T = []

        self.rhoxy = [[], [], [], []]
        self.rhoyx = [[], [], [], []]

        self.phixy = [[], []]
        self.phiyx = [[], []]

        self.RZxx = [[], []]
        self.RZxy = [[], []]
        self.RZyx = [[], []]
        self.RZyy = [[], []]

        self.IZxx = [[], []]
        self.IZxy = [[], []]
        self.IZyx = [[], []]
        self.IZyy = [[], []]

        self.activated = []


def make_file_pplt(path_file_zss, site, band):

    window_site = FilePPLT()

    # ============= rho xy ==================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rho', 'xy')
    window_site.rhoxy = [parameter, E1, E2, E3, E4]
    window_site.T = T

    # ============= rho yx ==================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rho', 'yx')
    window_site.rhoyx = [parameter, E1, E2, E3, E4]

    # ============= phi xy ==================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'phi', 'xy')
    window_site.phixy = [parameter, E1]

    # ============= phi yx ==================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'phi', 'yx')
    window_site.phiyx = [parameter, E1]


    # ============= RZ xx ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoReal', 'xx')
    window_site.RZxx = [parameter, E1]

    # ============= RZ xy ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoReal', 'xy')
    window_site.RZxy = [parameter, E1]

    # ============= RZ yx ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoReal', 'yx')
    window_site.RZyx = [parameter, E1]

    # ============= RZ yy ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoReal', 'yy')
    window_site.RZyy = [parameter, E1]


    # ============= IZ xx ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoImag', 'xx')
    window_site.IZxx = [parameter, E1]

    # ============= IZ xy ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoImag', 'xy')
    window_site.IZxy = [parameter, E1]

    # ============= IZ yx ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoImag', 'yx')
    window_site.IZyx = [parameter, E1]

    # ============= IZ yy ====================================================
    T, parameter, E1, E2, E3, E4 = read_file_zss(path_file_zss, 'rhoImag', 'yy')
    window_site.IZyy = [parameter, E1]


    name_rate = path_file_zss.split('/')
    window_site.name = name_rate[1]
    window_site.rate = name_rate[0]
    window_site.name_plot = window_site.name.replace("zss", "pplt")

    window_site.site = site
    window_site.color = [.2, .2, .2, 1]

    window_site.band = band

    for i in window_site.T:
        window_site.activated.append(False)

    return window_site

def save_file_pplt(FilePPLT):
    if os.path.isdir('PampaMT/file_pplt/' + FilePPLT.site):
        pass
    else:
        os.mkdir('PampaMT/file_pplt/' + FilePPLT.site)

    file_pplt = open('PampaMT/file_pplt/' + FilePPLT.site + '/' +
                     FilePPLT.rate + '_' + FilePPLT.name_plot, 'wb')

    pickle.dump(FilePPLT, file_pplt)
    file_pplt.close()


def read_file_zss(file_zss, parameter, component):

    get_parameter_zss = subprocess.getoutput('parametros-mt ' + file_zss + ' ' + parameter + '-' + component)

    if get_parameter_zss == 'formato de arquivo desconhecido':
        print(file_zss + ': Empty File - ' + parameter + '-' + component)
        return [], [], [], [], [], []

    elif get_parameter_zss == 'Segmentation fault (core dumped)':
        print(file_zss + ': Segmentation fault - ' + parameter + '-' + component)
        return [], [], [], [], [], []

    else:
        get_parameter_zss = get_parameter_zss.split('\n')

        element_T = []
        element_1 = []
        element_2 = []
        element_3 = []
        element_4 = []
        element_5 = []

        list_period = []

        for line in get_parameter_zss:

            list_period.append(line.split('\t'))

        for element in list_period:

            element_T.append(float(element[0]))
            element_1.append(float(element[1]))
            element_2.append(float(element[2]))
            if parameter == 'rho':
                element_3.append(float(element[3]))
                element_4.append(float(element[4]))
                element_5.append(float(element[5]))

    # print(a)
    # print(element_T)
    # print(element_1)
    # print(element_2)
    # print(element_3)
    # print(element_4)
    # print(element_5)

    return element_T, element_1, element_2, element_3, element_4, element_5


# fileplot = make_file_pplt('MT00256/bor602a054_10C.zss', 'bor602a')
# save_file_pplt(fileplot)
# print(fileplot.name)
# print(fileplot.name_plot)