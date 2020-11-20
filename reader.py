from pyhdf.SD import SD, SDC
import pprint
import requests
import re

def getFile(url):
    with requests.get(url, stream=True, allow_redirects = True) as r:
        r.raise_for_status()
        l = r.text
        print(l)
        exp = re.findall('>([0-9]{4}\.[0-9]{2}.[0-9]{2})',l)

        for date in exp:
            pass

file_name = 'test.hdf'
file = SD(file_name, SDC.READ)

def scale(data, items):
    for key, value in items:
        if key == 'add_offset':
            add_offset = value  
        if key == 'scale_factor':
            scale_factor = value
    return (data - add_offset) * scale_factor
    
MOD13Q1_url = "https://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.006/"

getFile(MOD13Q1_url)

datasets_dic = file.datasets()

for idx,sds in enumerate(datasets_dic.keys()):
    print(idx,sds)

sds_obj = file.select('250m 16 days NDVI') # select sds

data = sds_obj.get() # get sds data
print("\n","A")
azimuth = file.select('250m 16 days relative azimuth angle')
pprint.pprint(azimuth.attributes())
azimuth_data = azimuth.get()

view = file.select('250m 16 days view zenith angle')
pprint.pprint(view.attributes())
view_data = view.get()

sun = file.select('250m 16 days sun zenith angle')
pprint.pprint(sun.attributes())
sun_data = sun.get()

print()

print("(" + str(len(sun_data)) + "," + str(len(sun_data[0])) + ")")
print("Scaled data")
print("azimuth\n",scale(azimuth_data,azimuth.attributes().items()))
print("Zenith view\n",scale(view_data,view.attributes().items()))
print("Zenith sun\n",scale(sun_data,sun.attributes().items()))