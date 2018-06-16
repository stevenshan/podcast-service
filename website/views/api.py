# contains information for connecting to gPodder API

import requests # for making requests to api endpoints

HOST = "https://gpodder.net"
import os

# backups for testing without internet
class OfflineEndpoints:
    @staticmethod
    def search(query, headers):
        if query == "empty" or query == "none":
            return ""
        file = open("website/views/search-example.json").read()
        return file

# actual methods for connecting to api endpoints
class OnlineEndpoints(OfflineEndpoints):
    @staticmethod
    def search(query, headers):
        request = requests.get(
            HOST + "/search.json",
            params={"q": query},
            headers=headers
        )

        if request.status_code == 200:
            return request.content
        else:
            return None

# change between OfflineEndpoints and OnlineEndpoints
endpoints = OnlineEndpoints 
