import requests
from pyshex import ShExEvaluator, PrefixLibrary


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class MyPrefixLibrary(PrefixLibrary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_namespace(self, ns):
        """
        Describe our own method to retrieve ns.
        Used to handle empty namespaces, e.g. ''
        """
        return self.__getattribute__(ns)
