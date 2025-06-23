import requests
requests.packages.urllib3.disable_warnings() 

class Netbox:
    def __init__(self, **kwargs):
        try:
            self.header = {"Authorization": "Token " + kwargs.pop("token"), "Content-Type": "application/json"}
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
            response = requests.get(fullUrl, headers=self.header, params=params, verify=False)
            response.raise_for_status()
            return response.json()["results"]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GET request failed: {e}")

    def patch(self, *, uri: str, params: dict):
        """
        Perform a PATCH request against a specific NetBox API endpoint, or a list of endpoints including the ID value. Only required to specify parameters being updated on the object.

        You can update these via a list (for a single, or multiple endpoints), or you can pass it a single dictionary to a single endpoint:
        1. Via a list:
        uri: /some/endpoint
        [{
            "id": x,
            "key": "value"
        }]

        2. Via a dictionary to a specific endpoint via URI:
        uri: /some/endpoint/123
        {
            "key": "value"
        }

        Args:
            uri (str): The API path after /api/, e.g., 'dcim/devices/{id}'.
            params (dict): The parameters to update on the object.

        Returns:
            HTTP code I think?
        """
        fullUrl = self.urlBase + uri.lstrip("/")  # ensure no double slashes
        try:
            response = requests.patch(fullUrl, headers=self.header, json=params, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"PATCH request failed: {e}")

    def put(self, *, uri: str, params):
        """
        Perform a PUT request against NetBox API endpoints or a list of endpoints. Entire object required to be specified within each list item.

        Args:
            uri (str): The API path after /api/, e.g., 'dcim/devices/'.
            params (list): The list of objects update.

        Returns:
            HTTP code I think?
        """
        fullUrl = self.urlBase + uri.lstrip("/")  # ensure no double slashes
        try:
            response = requests.put(fullUrl, headers=self.header, json=params, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"PUT request failed: {e}")

    def getDeviceRoles(self, filters: dict = None):
        """
        Retrieve device roles from NetBox, optionally applying filters.

        Args:
            filters (dict, optional): Filter parameters like {"slug": "router"}

        Returns:
            list: Device role objects.
        """
        return self.get(uri="dcim/device-roles", params=filters)

    def getDevices(self, filters: dict = None):
        """
        Retrieve devices from NetBox, optionally applying filters.

        Args:
            filters (dict, optional): Filter parameters like {"name": "deviceName"}

        Returns:
            list: Device objects.
        """
        return self.get(uri="dcim/devices", params=filters)

    def getPrefixes(self, filters: dict = None):
        """
        Retrieve IPAM prefixes from Netbox, optionally applying filters.

        Args:
            filters (dict, optional): Filter parameters like {"prefix":"w.x.y.z/ab"}

        Returns:
            list: Prefix objects.
        """
        return self.get(uri="ipam/prefixes", params=filters)

    def getIpAddresses(self, filters: dict = None):
        """
        Retrieve IP addresses from Netbox, optionally applying filters.

        Args:
            filters (dict, optional): Filter parameters like {"parent":"w.x.y.z/ab"}

        Returns:
            list: IP address objects
        """
        return self.get(uri="ipam/ip-addresses", params=filters)

    def updateIpAddresses(self, addresses: list):
        """
        Update IP address objects with specified criteria.

        Args:
            addresses (list, mandatory): List of address objects with updated values like {"id": x, "dns_name": "hostname"}

        Returns:
            HTTP code
        """
        return self.put(uri="ipam/ip-addresses/", params=addresses)