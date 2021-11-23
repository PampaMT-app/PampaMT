#!/usr/bin/python3

import os
import sys

user = os.environ['HOME']
sys.path.append(user + '/.PampaMT')

if os.path.isdir(user + '/.PampaMT'):

    if len(sys.argv) > 1:

        if sys.argv[1] == 'update':

            from update.update import update
            print('Update processing ...')
            update()

        elif sys.argv[1] == 'remove':
            from install.remove_pampamt import remove
            remove()
        else:
            print('Use: \n'
                  'Open PampaMT: \n'
                  '     pampamt \n'
                  ' \n'
                  'Update PampaMT: \n'
                  '     pampamt update \n'
                  ' \n'
                  'Uninstall PampaMT: \n'
                  '     pampamt remove \n')

    else:
        os.chdir(user + '/.PampaMT')
        os.system('./bin/open_pampamt')


else:
    print('The PampaMT is a Software to pre-processing MT data.\n'
          'The following packages will be installed:\n'
          'git, python-kivy, python3-kivy,  python3-dev, libsdl2{,-image,-mixer,-ttf}-dev python3-matplotlib\n'
          '\n'
          'If your Ubuntu version is 17 or 18, will be installed the developed version')
    perm_install = input('Do you want to install PampaMT? (Y/n): ')
    if perm_install in ['Y', 'y', 'S', 's']:

        os.system('sudo apt-get install git python3-matplotlib')# python-dev libsdl2{,-image,-mixer,-ttf}-dev')
        os.system('sudo add-apt-repository ppa:kivy-team/kivy-daily')
        os.system('sudo apt-get install python3-kivy')
        os.system('sudo apt-get install libsdl2-dev')
        os.system('sudo apt-get install libsdl2-image-dev')

        print('\n')
        print('Will be downloader from PampaMT (GitHub)')
        os.chdir(user)

        os.system('git clone https://github.com/PatrickRogger/PampaMT.git .PampaMT')
        os.chdir(user + '/.PampaMT')


        from install.install_pampamt import install
        install()
    else:
        print('Exit PampaMT')