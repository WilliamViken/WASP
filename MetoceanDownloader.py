
#  Copyright (c) 2022, NTNU
#  Author: Benjamin Lagemann, benjamin.lagemann@ntu.no

import copy
import math
from time import strftime

import cftime
import xarray
import copernicus
import xarray as xr
from collections import defaultdict
import pydap.lib
import timeit


class MetoceanDownloader:
    _username: str
    _password: str

    #_active_waves_dataset: xarray.Dataset  # active dataset in cache
    _active_wind_dataset: xarray.Dataset  # active wind dataset in cache

    def __init__(self, username: str, password: str, caching=True):
        self._username = username
        self._password = password
       # self.connect_to_wave_data()
        self.connect_to_wind_data()

        if caching:
            pydap.lib.CACHE = "/tmp/pydap-cache/"  # activate caching

    def connect_to_wave_data(self, dataset_id: str = 'cmems_mod_glo_wav_my_0.2_PT3H-i'):
        print("Establishing connection to wave data")
        # DATASET_ID = 'global-analysis-forecast-wav-001-027' # from 2019
        # default dataset until 2019

        # open data store
        data_store = copernicus.copernicusmarine_datastore(dataset_id, self._username, self._password)

        # inspect dataset
        dataset = xr.open_dataset(data_store)
        self._active_waves_dataset = dataset

        # assert all important variables are included in the dataset
        assert ("VHM0" in dataset)  # sea_surface_wave_significant_height
        assert ("VMDR" in dataset)  # sea_surface_wave_from_direction
        assert ("VTPK" in dataset)  # Wave period at spectral peak / peak period

        print("Connection to wave data established")

    def connect_to_wind_data(self, dataset_id: str = "CERSAT-GLO-BLENDED_WIND_L4_REP-V6-OBS_FULL_TIME_SERIE"):
        print("Establishing connection to wind data")

        # open data store
        data_store = copernicus.copernicusmarine_datastore(dataset_id, self._username, self._password)

        # inspect dataset
        dataset = xr.open_dataset(data_store)
        self._active_wind_dataset = dataset

        # TODO asserts
        # assert all important variables are included in the dataset
        # assert ("VHM0" in dataset)  # sea_surface_wave_significant_height
        # assert ("VMDR" in dataset)  # sea_surface_wave_from_direction
        print("Connection to wind data established")

    def get_weather(self, time_input: cftime, latitude: float, longitude: float) -> dict:
        print("Requesting weather data for: " + cftime.datetime.strftime(time_input,
                                                                         format="%Y-%m-%dT%H:%M:%S") + " | Latitude " + str(
            latitude) + " | Longitude: " + str(longitude))
        # TODO assert time is within bounds
        start_time = timeit.default_timer()

        # assert position is within bounds
        assert (latitude <= 90)
        assert (latitude >= -90)
        assert (longitude >= -180)
        assert (longitude < 180)

        # assemble time
        # time = '2013-01-01T00:00:00.000000000'
        time = cftime.datetime.strftime(time_input, format="%Y-%m-%dT%H:%M:%S.000000000")

        # get wave data
        #subset_waves = self._active_waves_dataset.interp(time=time, latitude=latitude, longitude=longitude)

        # read out values
        # how select data from xarray: https://xarray.pydata.org/en/stable/user-guide/indexing.html
        # see https://catalogue.marine.copernicus.eu/documents/PUM/CMEMS-GLO-PUM-001-032.pdf for variables and units
        #signifcant_wave_height = float(subset_waves.VHM0.data)
        #wave_direction = float(subset_waves.VMDR.data)
        #peak_period = float(subset_waves.VTPK.data)

        # get wind data
        subset_wind = self._active_wind_dataset.interp(time=time, lat=latitude, lon=longitude)

        # read out values
        northward_wind = float(subset_wind.northward_wind)
        eastward_wind = float(subset_wind.eastward_wind)

        # process values
        wind_direction: float = 360.0 - (math.degrees(math.atan2(eastward_wind, northward_wind)) + 180.0)  # TODO double-check wind direction
        wind_speed: float = math.sqrt(northward_wind ** 2 + eastward_wind ** 2)

        print("Request time: %s seconds" % (round(timeit.default_timer() - start_time, 1)))

        # compile dict
        weather_dict: dict = defaultdict(dict)  # create default dict (enables special access/append functions)

       # weather_dict["significant wave height"]["unit"] = "m"
        #weather_dict["significant wave height"]["value"] = signifcant_wave_height
       # weather_dict["mean wave direction"]["unit"] = "deg"
       # weather_dict["mean wave direction"]["value"] = wave_direction
       # weather_dict["wave peak period"]["unit"] = "s"
       # weather_dict["wave peak period"]["value"] = peak_period
        weather_dict["wind direction in 10m height"]["unit"] = "deg"
        weather_dict["wind direction in 10m height"]["value"] = wind_direction
        weather_dict["wind speed in 10m height"]["unit"] = "m/s"
        weather_dict["wind speed in 10m height"]["value"] = wind_speed

        return weather_dict
