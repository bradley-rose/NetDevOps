import Netbox.netboxApi as nbApi
from pykeepass import PyKeePass

secrets = PyKeePass("Secrets/secrets.kdbx", keyfile="Secrets/secrets.keyx")

def getDnsNames(nb, cidr):
    results = nb.getIpAddresses({
        "parent": cidr
    })

    for address in results:
        print(address["address"])
        print("\t" + address["dns_name"])

def main():
    # Write your executing code here
    nb = nbApi.Netbox(
        token = secrets.find_entries(path=["Netbox", "API Key"]).password,
        url = secrets.find_entries(path=["Netbox", "URL"]).password
    )
    
    # Write your executing code in here.
    

if __name__ == "__main__":
    main()