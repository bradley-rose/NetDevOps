import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings() 

class OPNsense:
    def __init__(self, **kwargs):
        try:
            self.username = kwargs.pop("key")
            self.password = kwargs.pop("secret")
            self.urlBase = "https://" + kwargs.pop("url") + "/api/"
        except KeyError as e:
            raise TypeError(f"Missing required argument: '{e.args[0]}'")

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, *, uri: str, params: dict = None):
        """
        Perform a GET request against a specific NetBox API endpoint.
        
        Args:
            uri (str): The API path after /api/, e.g., 'dcim/devices/'.

        Returns:
            dict or list: Parsed JSON response from NetBox.
        """
        if not params:
            params = {}

        fullUrl = self.urlBase + uri.lstrip("/")  # ensure no double slashes
        try:
            response = requests.get(fullUrl, auth=HTTPBasicAuth(self.username, self.password), params=params)
            response.raise_for_status()
            return response.json()["results"]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GET request failed: {e}")

    def getFirewallAlias(self):
        return self.get(uri = "firewall/alias/get")