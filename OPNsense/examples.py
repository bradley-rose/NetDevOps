from pykeepass import PyKeePass
import opnsenseApi as opnApi
secrets = PyKeePass("../Secrets/secrets.kdbx", keyfile="../Secrets/secrets.keyx")

opnsense = opnApi.OPNsense(
    key=secrets.find_entries(path=["OPNsense", "API Key"]).password, 
    secret=secrets.find_entries(path=["OPNsense", "API Secret"]).password,
    url=secrets.find_entries(path=["OPNsense", "URL"]).password
)

print(opnsense.getFirewallAlias())