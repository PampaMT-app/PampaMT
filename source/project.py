from kivy.app import App
from kivy.uix.label import Label

import pickle

class ProjectPPMT():

    def __init__(self):

        self.name = ''
        self.sites = []
        self.path_file_ppmt = ''

        self.last_edit_site = ''

def save(project):
    file = open(project.path_file_ppmt, 'wb')
    pickle.dump(project, file)
    file.close()


def read_ppmt_file(path_file_ppmt):
    file = open(path_file_ppmt, 'rb')

    project = pickle.load(file)
    file.close()

    project.path_edit_site = path_file_ppmt

    return project


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! tirar depois
from source.site import Site

class ProjectTeste(ProjectPPMT):



    bor602a = Site()
    bor602a.name = 'bor602a'
    bor602a.equipment = 'ADU06'
    bor602a.project = 'zTest'

    bor602b = Site()
    bor602b.name = 'bor602b'
    bor602b.equipment = 'ADU06'
    bor602b.project = 'zTest'

    erg105a = Site()
    erg105a.name = 'erg105a'
    erg105a.equipment = 'ADU07'
    erg105a.project = 'zTest'

    list_site = [bor602a, bor602b, erg105a]

    def __init__(self):
        super(ProjectTeste, self).__init__()

        self.name = 'zTest'
        self.sites = self.list_site
        self.path_file_ppmt = '/home/patrick/zTest/zTest.ppmt'


class ErrorLoading(App):
    def build(self):

        lb_error = Label(text='Corrupted PPMT File\nCreate new PPMT File, type in terminal:\n'
                           '\n[i]pampamt-create[/i]')
        lb_error.markup = True


        return lb_error

# project = ProjectPPMT()
# project.project = 'Borborema'
# project.path_file_ppmt = '/home/patrick/.PampaMT/teste'
#
# project.save(

# arq = '/home/patrick/z16/z16.ppmt'
# #
# project = read_ppmt_file(arq)
# print(project.name)
# print(project.path_file_ppmt)
# lis_site = project.sites
#
# print(lis_site[1].name)
#
# lis_asc = lis_site[1].files_asc
#
# file = lis_asc[1]
# print(file.name)
# print(file.processingZ)

#make_file_band_asc(bor602a)