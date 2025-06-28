import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings() 

class OPNsense:
    def __init__(self, **kwargs):
        try:
            self.username = kwargs.pop("key")
            self.password = kwargs.pop("secret")
            self.urlBase = kwargs.pop("url") + "/api/"
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
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GET request failed: {e}")

    def post(self, *, uri: str, body: dict = None):
        if not body:
            body = {}
        
        fullUrl = self.urlBase + uri.lstrip("/")
        try:
            response = requests.post(fullUrl, auth=HTTPBasicAuth(self.username, self.password), json=body)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GET request failed: {e}")

    def getFirewallAliases(self):
        return self.get(uri = "firewall/alias/get")

    def getUnboundHostOverrides(self):
        return self.get(uri = "unbound/settings/search_host_override")

    def updateUnboundHostOverride(self, override):
        uri = "unbound/settings/set_host_override/" + override["uuid"]
        del override["rr"]
        return self.post(uri = uri, body = {"host":override})

    def createUnboundHostOverride(self, override):
        try:
            hostname = override.pop("hostname")
            server = override.pop("server")
            recordType = override.pop("type")
            description = override.pop("description")
            domain = override.pop("domain")

            if recordType not in ["A", "AAAA"]:
                raise ValueError("Value 'type' must be equal to 'A' or 'AAAA'.")

        except KeyError as e:
            raise TypeError(f"Missing required argument: '{e.args[0]}'")

        newOverride = {
            "hostname": hostname,
            "server": server,
            "rr": recordType,
            "domain": domain,
            "description": description,
            "enabled": 1
        }

        return self.post(uri = "unbound/settings/add_host_override", body = {"host":newOverride})

    def deleteUnboundHostOverride(self, override):
        return self.post(uri = "unbound/settings/del_host_override/" + override["uuid"])

    def applyUnboundChanges(self):
        return self.post(uri = "unbound/service/reconfigure")