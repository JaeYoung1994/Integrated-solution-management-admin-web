import requests

class Utils:
    @classmethod
    def requestUrl(self, method=str, url=str, data=None, json=None, params=None, **kwargs):
        method = method.upper()
        if method == "POST":
            res =requests.post(url=url, data=data, json=json, **kwargs)
        elif method == "GET":
            res = requests.get(url=url, params=params)
        return res