from fastapi import FastAPI
from requests import Session
from zeep.cache import InMemoryCache
from requests.auth import HTTPBasicAuth
import zeep
from zeep.transports import Transport
import os

env = os.environ
cache = InMemoryCache()
session = Session()
session.auth = HTTPBasicAuth(env['SOAP_USER'], env['SOAP_PASS'])

transport = Transport(session=session,
                      cache=cache)

client = zeep.Client(wsdl=env['SOAP_WSDL'],
                     transport=transport)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world!"}


@app.get("/getAllDevices")
def get_all_devices():
    return client.service.getAllDevices()


@app.get("/getAllDeviceGroups")
def get_all_device_groups():
    return client.service.GetAllDeviceGroups()


@app.get("/getAllDrivers")
def get_all_drivers():
    return client.service.getAllDrivers()


@app.get("/getAllGeoZones")
def get_all_geo_zones():
    return client.service.getAllGeoZones()

# getAllRoutes(dt from, dt to)
# @app.get("/getAllDevices")
# def read_item():
#     return json.dumps(client.service.getAllDevices())


@app.get("/getChannelDescriptors/{device_id}")
def get_channel_descriptors(device_id: int):
    return client.service.getChannelDescriptors(device_id)
