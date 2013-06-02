import sys
import time
from pprint import pprint

import requests

URI = "https://api.ninja.is/rest/v0/"
STREAM_URI = "https://stream.ninja.is/rest/v0/"
USER_ACCESS_TOKEN = sys.argv[1]
PARAMS = {"user_access_token": USER_ACCESS_TOKEN}

def put(path, *args, **kwargs):
    return requests.put(URI + path, *args, params=PARAMS, **kwargs)


def get(path, *args, **kwargs):
    p = PARAMS.copy()
    if "params" in kwargs:
        p.update(kwargs["params"])
        del kwargs["params"]

    return requests.get(URI + path, *args, params=p, **kwargs)


def stream_get(path, *args, **kwargs):
    return requests.get(STREAM_URI + path, *args, params=PARAMS, **kwargs)


def get_device_by_name(device_name):
    resource = "devices"
    r = get(resource)
    d = r.json()

    for device, value in d["data"].items():
        if value['default_name'] == device_name:
            return device, value


def set_DA(device, DA):
    r = put("device/" + device, data={"DA": DA})


def get_device_list():
    r = get("devices")
    return r.json()["data"]


def get_snapshot(webcam):
    r = stream_get('camera/%s/snapshot' % webcam)
    pprint(r)
    print dir(r)
    pprint(r.text)
    pprint(r.raw)
    pprint(r.url)
    pprint(r.content)


def get_data_stream(device, minutes, interval, fn):
    print "device/%s/data" % device
    now = int(1000*time.time())
    params = {"fn": fn,
              "interval": interval,
              "from": now - 60*minutes*1000,
              "to": now}
    r = get("device/%s/data" % device, params=params)
    return [d["v"] for d in r.json()["data"]]


def main():
    devices = get_device_list()
    for name, data in devices.items():
        print name, data['default_name']
    webcam_id, webcam = get_device_by_name("Web Cam")
    pprint(webcam)
    # get_snapshot(webcam_id)

    temp_id, temp = get_device_by_name("Temperature")
    data = get_data_stream(temp_id, 120, "5min", "count")
    print data


if __name__ == '__main__':
    main()
