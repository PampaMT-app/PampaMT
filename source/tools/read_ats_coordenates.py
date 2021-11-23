"""
Tools PampaMT
Author: Patrick Rogger Garcia
Date: 2018/07/31

Reads ats files coordinates
"""

from glob import glob
from subprocess import getoutput


def read_ats_coordinates(path_ats_files):

    """
    :param path_ats_files: Path content all ats files
    :return: Dictionary with Latitude, Longitude and Elevation
    """

    list_latitude = []
    list_longitude = []
    list_elevation = []

    print(path_ats_files)

    # get ats files
    list_ats_files = glob(path_ats_files + '/*.ats')

    for file in list_ats_files:
        lat = float(getoutput('atsheader ' + file + ' Latitude'))
        long = float(getoutput('atsheader ' + file + ' Longitude'))
        elev = float(getoutput('atsheader ' + file + ' Elevation'))

        # Test: if lat and long unregistered
        if lat == 0 and long == 0:
            pass
        else:
            list_latitude.append(lat)
            list_longitude.append(long)
            list_elevation.append(elev)

    # Returns the Mean of lists

    try:

        Coordinates = {}
        Coordinates['Latitude'] = sum(list_latitude) / len(list_latitude)
        Coordinates['Longitude'] = sum(list_longitude) / len(list_longitude)
        Coordinates['Elevation'] = sum(list_elevation) / len(list_elevation)

    except ZeroDivisionError:
        Coordinates = {}
        Coordinates['Latitude'] = 0
        Coordinates['Longitude'] = 0
        Coordinates['Elevation'] = 0

    return Coordinates
