import os

user = os.environ['HOME']

# ========================= TEST ==================
#os.chdir('/home/patrick/PampaMT/PROC_MT/zTest')

# Class to create Sites
class Site():
    def __init__(self):
        self.name = ''
        self.path_origin = ''
        self.equipment = ''
        self.project = ''
        self.coordinates = {}
        self.tojones = ''

        self.copy = False
        self.ats2asc = False

        self.files_plot = {}
        self.files_asc = []
        self.files_zss = {}

class FileAsc():

    def __init__(self):
        self.name = ''
        self.site = ''
        self.equipment = ''
        self.project = ''
        self.band = ''
        self.processingZ = False
        self.remote_reference = ''



