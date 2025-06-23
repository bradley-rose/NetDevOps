import netboxApi
from pykeepass import PyKeePass

secrets = PyKeePass("secrets.kdbx", keyfile="secrets.keyx")

def getDnsNames(nb, cidr):
    results = nb.getIpAddresses({
        "parent": cidr
    })

    for address in results:
        print(address["address"])
        print("\t" + address["dns_name"])

def updateDnsNames(nb):
    results = nb.getIpAddresses()

    addressesToUpdate = []
    for address in results:
        if address["dns_name"] and not ".yourDomain.xyz" in address["dns_name"]:
            address["dns_name"] += ".yourDomain.xyz"
            addressesToUpdate.append(address)

    nb.updateIpAddresses(addresses=addressesToUpdate)

if __name__ == "__main__":
    nb = netboxApi.Netbox(
        token = secrets.find_entries(path=["Netbox API Key"]).password,
        url = secrets.find_entries(path=["Netbox URL"]).password
    )
    
    # Write your executing code in here.
    main()