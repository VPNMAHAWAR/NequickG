import matplotlib.pyplot as plt
import numpy as np
import csv
from mpl_toolkits.basemap import Basemap
from NequickG import NEQTime, Position, GalileoBroadcast, NequickG
from  NequickG_global import  NequickG_global

def Task1():
    time = [10, 12]

    TX = NEQTime(4,12)

    BX = GalileoBroadcast(236.831,0,0)
    RX = Position(40,0)
    NEQ_global = NequickG_global(TX,BX)
    NEQ, Para = NEQ_global.get_Nequick_local(RX)

    hmin = 100
    hmax = 1000
    hs = np.arange(hmin, hmax)

    N = NEQ.electrondensity(hs)
    #plt.figure()
    Azr = Para.Azr
    label = "Azr" + str(int(Azr)) + " Apr 12UT 40N 0E"

    plt.plot(hs, N, label = label)
    plt.xlabel('Height(km)')
    plt.ylabel("Electron Density (m^-3)")

    plt.title("Nequick-G:\n" + " Apr 12UT ")
    plt.grid()
    plt.legend()
    plt.show()
    # Task1()

def Task1_2():

    TX = NEQTime(4,12)

    BX = GalileoBroadcast(236.831,0,0)
    RX = Position(40,0)
    NEQ_global = NequickG_global(TX,BX)
    NEQ, Para = NEQ_global.get_Nequick_local(RX)

    hmin = 100
    hmax = 1000
    hs = np.arange(hmin, hmax)

    N = NEQ.electrondensity(hs)
    #plt.figure()
    Azr = Para.Azr
    label = "Azr" + str(int(Azr)) + " Apr 12UT 40N 0E"

    plt.plot(hs, N, label = label)
    plt.xlabel('Height(km)')
    plt.ylabel("Electron Density (m^-3)")

    iri_hs = np.load('iri_hs.npr')
    iri_ns = np.load('iri_ns.npr')
    plt.plot(iri_hs, iri_ns * 10**6, label = 'iri')

    plt.title("Nequick-G:\n" + " Apr 12UT ")
    plt.grid()
    plt.legend()
    plt.show()

# Task1_2()

def Task1_3():
    TX = NEQTime(4,12)

    BX = GalileoBroadcast(193,0,0)
    RX = Position(0,0)
    NEQ_global = NequickG_global(TX,BX)
    NEQ, Para = NEQ_global.get_Nequick_local(RX)

    hmin = 60
    hmax = 2000
    hs = np.linspace(hmin, hmax, 195)

    N = NEQ.electrondensity(hs)

    out = np.empty((195,5))
    out[:,0] = 6371.2 + hs
    out[:,1] = hs
    out[:,2] = 40
    out[:,3] = 0
    out[:,4] = N

    out = out.tolist()

    with open('NequickG.out', 'w') as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerows(out)

Task1_3()

def Task1_1():
    # TASK 1: Plot NequickG at 8 different locations

    time = [10, 12]
    positions = [
        [0, 0],
        [15, 0],
        [30, 0],
        [45, 0],
        [60, 0],
        [75, 0]]
    broadcasts = [[200,0,0]]
    TX = NEQTime(*time)
    for bx in broadcasts:
        BX = GalileoBroadcast(*bx)
        for pos in positions:

            RX = Position(*pos)
            NEQ_global = NequickG_global(TX,BX)
            NEQ, Para = NEQ_global.get_Nequick_local(RX)

            hmin = 100
            hmax = 1000
            h = np.arange(hmin, hmax)

            N = NEQ.electrondensity(h)
            #plt.figure()
            Azr = Para.Azr
            label = "Azr" + str(int(Azr)) + " Oct 12UT " + str(pos[0]) + "N " + str(pos[1]) + "E"

            plt.plot(h, N, label = "Azr" + str(int(Azr))+ " " + str(pos[0]) + "N")
    plt.xlabel('Height(km)')
    plt.ylabel("Electron Density (m^-3)")

    plt.title("Nequick-G:\n" + " Oct 12UT ")
    plt.grid()
    plt.legend()
    plt.savefig('profiles/200Az.png')


def Task2():
    #test vTEC
    TX = NEQTime(4,12)
    RX = Position(40,0)
    BX = GalileoBroadcast(236.831,0,0)
    NEQ_global = NequickG_global(TX, BX)
    NEQ, Para = NEQ_global.get_Nequick_local(RX)
    print NEQ.vTEC(100, 2000)

# Task2()

def Task3():
    # vTEC map
    BX = GalileoBroadcast(80,0,0)
    vTEC = []
    for lat in np.arange(40, 60, 0.5):
        vTEC_lon = []
        for lon in range(-20, 20, 1):
            pos = [lat, lon]
            TX = NEQTime(10, 12)
            RX = Position(*pos)
            NEQ_global = NequickG_global(TX, BX)
            NEQ, para = NEQ_global.get_Nequick_local(RX)
            vTEC_lon.append(NEQ.map_vTEC(100, 1000))
        vTEC.append(vTEC_lon)
    plt.figure()
    plt.contour(vTEC)
    plt.show()


def Task4():
    # set up orthographic map projection with
    # perspective of satellite looking down at 50N, 100W.
    # use low resolution coastlines.
    plt.figure()
    mapp = Basemap(projection='ortho',lat_0=43,lon_0=1.4,resolution='l')
    # draw coastlines, country boundaries, fill continents.
    mapp.drawcoastlines(linewidth=0.25)
    mapp.drawcountries(linewidth=0.25)
    mapp.fillcontinents(color='coral',lake_color='aqua')
    # draw the edge of the map projection region (the projection limb)
    mapp.drawmapboundary(fill_color='aqua')
    # draw lat/lon grid lines every 30 degrees.
    mapp.drawmeridians(np.arange(0,360,30))
    mapp.drawparallels(np.arange(-90,90,30))

    BX = GalileoBroadcast(80,0,0)
    TX = NEQTime(10, 12)
    NEQ_global = NequickG_global(TX, BX)
    latlat, lonlon, vTEC = NEQ_global.map(00, -60, 60, 60, resolution=60)

    xx, yy = mapp(lonlon, latlat)
    # xx, yy = mapp(latlat, lonlon)

    cs = mapp.contour(xx, yy, vTEC, linewidths=1.5)
    # cs = mapp.contour(xx, yy, vTEC, linewidths=1.5, latlon = True)
    plt.title('vertical Total Electron Count over Toulouse')
    plt.show()

def Task4_2(TX, BX, folder):
    attrs = ['foF1', 'foF2', 'foE', 'M3000F2', 'NmF2', 'NmF1', 'NmE', 'hmE', 'hmF1', 'hmF2', 'modip',
             'Az','Azr', 'solarsine', 'solarcosine', 'chi', 'chi_eff', 'H0', 'B1bot', 'B1top', 'B2bot', 'BEtop', 'BEbot'
             ,'A1', 'A2', 'A3', 'k', 'vTEC']


    NEQ_global = NequickG_global(TX, BX)

    latlat, lonlon, outs = NEQ_global.map_parameters(attrs, -70, -180, 70, 180, resolution=150)


    for i in range(len(outs)):
        plt.figure()
        mapp = Basemap(projection='cyl',llcrnrlat= -90.,urcrnrlat= 90.,\
                  resolution='c',  llcrnrlon=-180.,urcrnrlon=180.)
        #-- draw coastlines, state and country boundaries, edge of map
        mapp.drawcoastlines()
        mapp.drawstates()
        mapp.drawcountries()

        #-- create and draw meridians and parallels grid lines
        mapp.drawparallels(np.arange( -90., 90.,30.),labels=[1,0,0,0],fontsize=10)
        mapp.drawmeridians(np.arange(-180.,180.,30.),labels=[0,0,0,1],fontsize=10)
        xx, yy = mapp(lonlon, latlat)

        cs = mapp.contourf(xx, yy, outs[i], linewidths=1.5)

        plt.title(attrs[i])
        mapp.colorbar(cs)
        plt.savefig('maps/' + folder + '/'+ attrs[i]+'.png')
        plt.close()


def Task4_3():
    # Low solar activity
    BX = GalileoBroadcast(2.580271,0.127628236,0.0252748384)
    # Medium solar activity
    # BX = GalileoBroadcast(121.129893,0.351254133,0.0134635348)
    # High solar activity
    # BX = GalileoBroadcast(236.831641, -0.39362878, 0.00402826613)
    # R12 = 150
    #BX = GalileoBroadcast(192.924,0,0)
    for time in [0, 4, 8, 12, 16, 20]:
        TX = NEQTime(4, time)
        Task4_2(TX, BX, 'low/'+ str(time))

# Task4_3()

def Task5():
    #test sTEC
    TX = NEQTime(10,12)
    BX = GalileoBroadcast(80,0,0)
    NEQ_global = NequickG_global(TX, BX)
    stec = NEQ_global.sTEC(100,40,0,1000,40,0)
    print stec

def Task6():
    #test sTEC
    TX = NEQTime(10,12)
    BX = GalileoBroadcast(80,0,0)
    NEQ_global = NequickG_global(TX, BX)
    stec = NEQ_global.sTEC2(100,40,0,1000,40,0)
    print stec

def Task7():
    # visualise the sTEC in the sky above toulouse

    TX = NEQTime(10,12)
    BX = GalileoBroadcast(80,0,0)
    NEQ_global = NequickG_global(TX, BX)

    # grid
    lat0 = 40
    lon0 = 0
    n = 5
    lats = np.linspace(-10,10, n) + lat0
    lons = np.linspace(-10, 10, n) + lon0

    stec = np.empty([n,n])

    for i in range(n):
        for j in range(n):
            print "j, i : " + str ((j, i))
            stec[j,i] = NEQ_global.sTEC(0, lat0, lon0, 20000, lats[i],lons[j])

    plt.imshow(stec)
    plt.show()


def Task8():
    TX = NEQTime(10,12)
    BX = GalileoBroadcast(80,0,0)
    NEQ_global = NequickG_global(TX, BX)
    pos = Position(40,0)
    NEQ, para = NEQ_global.get_Nequick_local(pos)
    print NEQ.vTEC_ratio()

# Task1()
