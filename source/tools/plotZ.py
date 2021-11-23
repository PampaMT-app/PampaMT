#!/usr/bin/python3

import matplotlib.pyplot as plt
from source.windowsite import FilePPLT, make_file_pplt

# path_files = glob.glob('PampaMT/file_pplt/' + site + '/*')
# files_active = []
# files = []
# for path_pplt in path_files:
#     arq = open(path_pplt, 'rb')
#     files.append(pickle.load(arq))
#     arq.close()
#
# for pplt in files:
#     if pplt.active_file == True:
#         files_active.append(pplt)
#
# print(files_active)

def export_matplotlib_jones(site):
    PPLT = make_file_pplt('final/' + site + '.dat', site=site, band='')

    size_point = 3

    T = PPLT.T
    rhoxy = PPLT.rhoxy[0]
    rhoyx = PPLT.rhoyx[0]

    phixy = []
    phiyx = []

    for phase in PPLT.phixy[0]:
        if phase < 0:
            phixy.append(phase + 180)
        else:
            phixy.append(phase)

    for phase in PPLT.phiyx[0]:
        if phase < 0:
            phiyx.append(phase + 180)
        else:
            phiyx.append(phase)


    RZxx = PPLT.RZxx[0]
    IZxx = PPLT.IZxx[0]

    RZxy = PPLT.RZxy[0]
    IZxy = PPLT.IZxy[0]

    RZyx = PPLT.RZyx[0]
    IZyx = PPLT.IZyx[0]

    RZyy = PPLT.RZyy[0]
    IZyy = PPLT.IZyy[0]


    T_min = 1e-4
    T_max = 1e4

    phi_min = 0
    phi_max = 180

    rho_min = 1e-1
    rho_max = 1e5

    Zxx_min = min([min(RZxx), min(IZxx)]) - max([max(RZxx), max(IZxx)])*.2
    Zxx_max = max([max(RZxx), max(IZxx)]) + max([max(RZxx), max(IZxx)])*.2

    Zxy_min = min([min(RZxy), min(IZxy)]) - max([max(RZxy), max(IZxy)])*.2
    Zxy_max = max([max(RZxy), max(IZxy)]) + max([max(RZxy), max(IZxy)])*.2

    Zyx_min = min([min(RZyx), min(IZyx)]) - max([max(RZyx), max(IZyx)])*.2
    Zyx_max = max([max(RZyx), max(IZyx)]) + max([max(RZyx), max(IZyx)])*.2

    Zyy_min = min([min(RZyy), min(IZyy)]) - max([max(RZyy), max(IZyy)])*.2
    Zyy_max = max([max(RZyy), max(IZyy)]) + max([max(RZyy), max(IZyy)])*.2

    Txy_min = -40
    Txy_max = 40

    Tyx_min = -40
    Tyx_max = 40

    fig = plt.figure()
    fig.set_size_inches(19, 10.5, forward=True)



    prho = fig.add_subplot(231)
    prho.set_aspect('equal')
    prho.plot(T, rhoxy, 's', T, rhoyx, 'o', ms=size_point)
    prho.grid()
    prho.set_xlim(T_min, T_max)
    prho.set_ylim(rho_min, rho_max)
    prho.set_xscale('log')
    prho.set_yscale('log')
    prho.set_title(r'$\rho$')
    prho.legend((r'$\rho_{xy}$', r'$\rho_{yx}$'), loc='upper right')


    pphi = fig.add_subplot(234)
    #pphi.plot(T, phixy, 's', T, phiyx, 'o', ms=size_point)
    pphi.grid()
    pphi.set_xlim(T_min, T_max)
    pphi.set_ylim(phi_min, phi_max)
    pphi.set_xscale('log')
    pphi.set_title(r'$\phi$')
    pphi.errorbar(T, phixy, yerr=PPLT.phixy[1], fmt='s', ms=size_point)
    pphi.errorbar(T, phiyx, yerr=PPLT.phiyx[1], fmt='o', ms=size_point)
    pphi.legend((r'$\phi_{xy}$', r'$\phi_{yx}$'), loc='upper right')


    pZxx = fig.add_subplot(332)
    #pZxx.plot(T, RZxx, 's', T, IZxx, 'o', ms=size_point)
    pZxx.grid()
    pZxx.set_xlim(T_min, T_max)
    pZxx.set_ylim(Zxx_min, Zxx_max)
    pZxx.set_xscale('log')
    pZxx.set_title(r'$Z_{xx}$')
    pZxx.errorbar(T, RZxx, yerr=PPLT.RZxx[1], fmt='s', ms=size_point)
    pZxx.errorbar(T, IZxx, yerr=PPLT.IZxx[1], fmt='o', ms=size_point)
    pZxx.legend((r'$\Re_{xx}$', r'$\Im_{xx}$'), loc='upper right')

    pZxy = fig.add_subplot(333)
    #pZxy.plot(T, RZxy, 's', T, IZxy, 'o', ms=size_point)
    pZxy.grid()
    pZxy.set_xlim(T_min, T_max)
    pZxy.set_ylim(Zxy_min, Zxy_max)
    pZxy.set_xscale('log')
    pZxy.set_title(r'$Z_{xy}$')
    pZxy.errorbar(T, RZxy, yerr=PPLT.RZxy[1], fmt='s', ms=size_point)
    pZxy.errorbar(T, IZxy, yerr=PPLT.IZxy[1], fmt='o', ms=size_point)
    pZxy.legend((r'$\Re_{xy}$', r'$\Im_{xy}$'), loc='upper right')

    pZyx = fig.add_subplot(335)
    #pZyx.plot(T, RZyx, 's', T, IZyx, 'o', ms=size_point)
    pZyx.grid()
    pZyx.set_xlim(T_min, T_max)
    pZyx.set_ylim(Zyx_min, Zyx_max)
    pZyx.set_xscale('log')
    pZyx.set_title(r'$Z_{yx}$')
    pZyx.errorbar(T, RZyx, yerr=PPLT.RZyx[1], fmt='s', ms=size_point)
    pZyx.errorbar(T, IZyx, yerr=PPLT.IZyx[1], fmt='o', ms=size_point)
    pZyx.legend((r'$\Re_{yx}$', r'$\Im_{yx}$'), loc='upper right')

    pZyy = fig.add_subplot(336)
    #pZyy.plot(T, RZyy, 's', T, IZyy, 'o', ms=size_point)
    pZyy.grid()
    pZyy.set_xlim(T_min, T_max)
    pZyy.set_ylim(Zyy_min, Zyy_max)
    pZyy.set_xscale('log')
    pZyy.set_title(r'$Z_{yy}$')
    pZyy.errorbar(T, RZyy, yerr=PPLT.RZyy[1], fmt='s', ms=size_point)
    pZyy.errorbar(T, IZyy, yerr=PPLT.IZyy[1], fmt='o', ms=size_point)
    pZyy.legend((r'$\Re_{yy}$', r'$\Im_{yy}$'), loc='upper right')


    Zxx = [3,4]
    Tt = [3,4]

    # pTxy = fig.add_subplot(338)
    # pTxy.plot(Tt, Zxx, 's', Tt, Zxx, 'o', ms=size_point)
    # pTxy.grid()
    # pTxy.set_xlim(T_min, T_max)
    # pTxy.set_ylim(Txy_min, Txy_max)
    # pTxy.set_xscale('log')
    # pTxy.set_title('Tzx')
    # pTxy.legend((r'$\Re_{zx}$', r'$\Im_{zx}$'), loc='upper right')
    #
    # pTyx = fig.add_subplot(339)
    # pTyx.plot(Tt, Zxx, 's', Tt, Zxx, 'o', ms=size_point)
    # pTyx.grid()
    # pTyx.set_xlim(T_min, T_max)
    # pTyx.set_ylim(Tyx_min, Tyx_max)
    # pTyx.set_xscale('log')
    # pTyx.set_title('Tzy')
    # pTyx.legend((r'$\Re_{zy}$', r'$\Im_{zy}$'), loc='upper right')

    plt.subplots_adjust(left=.04, bottom=.06, right=.98, top=.94, wspace=0.16, hspace=0.31)

    plt.savefig('final/' + site + '/' + site + '-J.png', dpi=300)

    plt.show()

