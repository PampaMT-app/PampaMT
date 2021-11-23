#!/usr/bin/python3

import os
import glob

user = os.environ['HOME']

def install():
    os.system('chmod +x bin/*')
    os.system('chmod +x install/*')
    os.system('chmod +x update/*')
    os.system('chmod +x main.py')
    os.system('chmod +x PampaMT.py')

    error_language = True
    while error_language:
        language = input('Set language (en_US/pt_BR): ')
        if language in ['en_US', 'pt_BR']:
            error_language = False
            print('Language = ' + language)
            print('')
        else:
            print('[Error] ...')
            print('')

    arq_dic_language = open(user + '/.PampaMT/file/set_language', 'w')
    arq_dic_language.write(language + '.dic')
    arq_dic_language.close()

    error_set_bash = True
    while error_set_bash:
        terminal = input('Do you want the terminal to open when you start PampaMT (Y/n)?: ')
        if terminal in ['Y', 'y', 'S', 's']:
            terminal_open = 'true'
            error_set_bash = False
        elif terminal in ['N', 'n']:
            terminal_open = 'false'
            error_set_bash = False
        else:
            print('Error ...')
            print('')

    arq_desktop = open(user + '/.local/share/applications/pampamt.desktop', 'w')
    arq_desktop.write('[Desktop Entry]\n'
                      'Version=0.1.0\n'
                      'Type=Application\n'
                      'Name=PampaMT\n'
                      'Exec="' + user + '/.PampaMT/bin/open_pampamt" %f\n'
                      'Icon=' + user + '/.PampaMT/image/logo3.png\n'
                      'Comment=App to Processing Magnetotelluric Data\n'
                      'Categories=Processing;MT;\n'
                      'Terminal=' + terminal_open +'\n'
                      'StartupNotify=true\n'
                      'StartupWMClass=pampamt\n')
    arq_desktop.close()

    if os.path.isdir(user + '/PampaMT'):
        pass
    else:
        os.mkdir(user + '/PampaMT')

    if os.path.isdir(user + '/PampaMT/PROC_MT'):
        pass
    else:
        os.mkdir(user + '/PampaMT/PROC_MT')

    if os.path.isdir(user + '/PampaMT/DADOS_MT'):
        pass
    else:
        os.mkdir(user + '/PampaMT/DADOS_MT')


    if os.path.isdir(user + '/modelo'):
        os.mkdir(user + '/PampaMT/modelo')
        os.system('cp -r ' + user + '/modelo ' + user + '/PampaMT/')
        os.chdir(user + '/PampaMT')
    elif os.path.isfile(user + '/modelo.tar.xz'):
        os.system('cp ' + user + '/modelo.tar.xz ' + user + '/PampaMT/modelo.tar.xf')
        os.chdir(user + '/PampaMT')
        os.system('tar xf modelo.tar.xf')
        os.system('rm modelo.tar.xf')

    else:
        print("Copy the file 'modelo.tar.xf' to " + user)
        print('Please contact Patrick Rogger Garcia to obtain the processing model (modelo.tar.xf)')
        print('E-mail: patrick_rogger@hotmail.com')
        exit()

    list_dnff = []
    for path in os.get_exec_path():
        for dnff in glob.glob(path + '/*dnff*'):
            list_dnff.append(dnff)
    if len(list_dnff) == 0:
        print('Please install the EMTF package, visit:')
        print('http://mtnet.info/programs/egbert.html')
        exit()

    if os.path.isfile(user + '/bin/processamentoZ'):
        pass
    else:
        print('Please contact Patrick Rogger Garcia to obtain the processamentoZ')
        print('E-mail: patrick_rogger@hotmail.com')
        exit()

    if os.path.isfile(user + '/bin/parametros-mt'):
        pass
    else:
        print('Please contact Patrick Rogger Garcia to obtain the parametros-mt')
        print('E-mail: patrick_rogger@hotmail.com')
        exit()


    os.mkdir('modelo/PampaMT')
    os.mkdir('modelo/PampaMT/band_asc')
    os.mkdir('modelo/PampaMT/file_pplt')


    os.system('ln -s ~/.PampaMT/bin/pampamt.py  ~/bin/pampamt')

    print('Finish install PampaMT')
    print('Update PampaMT, type: pampamt update')
    print('Remove PampaMT, type: pampamt remove')
    print('')
    print('Type: pampamt')
