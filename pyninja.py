import sys
import time

import requests

URI = "https://api.ninja.is/rest/v0/"
USER_ACCESS_TOKEN = sys.argv[1]
PARAMS = {"user_access_token": USER_ACCESS_TOKEN}

def put(path, *args, **kwargs):
    return requests.put(URI + path, *args, params=PARAMS, **kwargs)


def get(path, *args, **kwargs):
    return requests.get(URI + path, *args, params=PARAMS, **kwargs)


def get_device_by_name(device_name):
    resource = "devices"
    r = get(resource)
    d = r.json()

    for device, value in d["data"].items():
        if value['default_name'] == device_name:
            return device, value


def set_DA(device, DA):
    r = put("device/" + device, data={"DA": DA})


def main():
    device, _ = get_device_by_name("Nina's Eyes")
    for _ in range(10):
        for colour in ["FF0000", "00FF00", "0000FF"]:
            set_DA(device, colour)


if __name__ == '__main__':
    main()
