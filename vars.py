
valid_set = ['vhi', 'prismc-tmax-daily', 'prismc-tmin-daily', 'prismc-precip-daily', 'rtma_dew_point-hourly',
             'rtma_pcp-hourly', 'rtma_temp-hourly', 'rtma_wind_u-hourly', 'rtma_wind_v-hourly', 'cpcc_precip_us-daily',
             'cpcc_precip_global-daily', 'cpcc_temp_max-daily', 'cpcc_temp_min-daily', 'chirpsc_final_05-daily',
             'chirpsc_final_25-daily',
             'chirpsc_prelim_05-daily', 'era5_land_2m_temp-hourly', 'era5_land_precip-hourly',
             'era5_land_surface_solar_radiation_downwards-hourly',
             'era5_land_snowfall-hourly', 'era5_land_wind_u-hourly', 'era5_land_wind_v-hourly',
             'era5_surface_runoff-hourly', 'era5_wind_100m_u-hourly',
             'era5_wind_100m_v-hourly', 'era5_volumetric_soil_water_layer_1-hourly']

VALID_DASHSET = []

for set in valid_set:
	if 'hourly' not in set:
		VALID_DASHSET.append({'label': set, 'value': set})
    else:
    	pass





TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI1MzQwMjMwMDc5OSwiaWF0IjoxNjMwNTMwMTgwLCJzdWIiOiJhMDIzYjUwYi0wOGQ2LTQwY2QtODNiMS1iMTExZDA2Mzk1MmEifQ.qHy4B0GK22CkYOTO8gsxh0YzE8oLMMa6My8TvhwhxMk'


