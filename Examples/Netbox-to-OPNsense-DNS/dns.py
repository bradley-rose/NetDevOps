
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Netbox import netboxApi as nbApi
from OPNsense import opnsenseApi as opnApi
from pykeepass import PyKeePass

secrets = PyKeePass("../../Secrets/secrets.kdbx", keyfile="../../Secrets/secrets.keyx")

nb = nbApi.Netbox(
    token = secrets.find_entries(path=["Netbox", "API Key"]).password,
    url = secrets.find_entries(path=["Netbox", "URL"]).password
)

opnsense = opnApi.OPNsense(
    key = secrets.find_entries(path=["OPNsense", "API Key"]).password,
    secret = secrets.find_entries(path=["OPNsense", "API Secret"]).password,
    url = secrets.find_entries(path=["OPNsense", "URL"]).password
)

def main():
    
    nbAddresses = nb.getIpAddresses()
    opnsenseOverrides = opnsense.getUnboundHostOverrides()["rows"]

    overrideChanges = {"create":[],"update":[],"delete":[],"none":[]}

    for nbAddress in (address for address in nbAddresses if address["dns_name"]):
        nbAddress["dns_name"] = nbAddress["dns_name"].split(".")[0]

        found = False
        for override in opnsenseOverrides:

            if nbAddress["address"].split("/")[0] == override["server"]:
                # Update if changes are necessary
                changes = False
                if not override["description"] == nbAddress["description"] or not override["hostname"] == nbAddress["dns_name"]:
                    changes = True

                if changes:
                    # Update existing entry, there are differences between Netbox and OPNsense
                    override["description"] = nbAddress["description"]
                    override["hostname"] = nbAddress["dns_name"]
                    override["domain"] = secrets.find_entries(path=["Domain"]).password
                    overrideChanges["update"].append(override)
                    found = True
                    break

                else:
                    # Take no action, Netbox entry matches OPNsense override
                    overrideChanges["none"].append(override)
                    found = True
                    break
                    
        if not found:
            # Create new unbound override
            override = {
                "hostname": nbAddress["dns_name"],
                "description": nbAddress["description"],
                "domain": secrets.find_entries(path=["Domain"]).password,
                "server": nbAddress["address"].split("/")[0]
            }
            if nbAddress["family"]["label"] == "IPv4":
                override["type"] = "A"
            elif nbAddress["family"]["label"] == "IPv6":
                override["type"] = "AAAA"

            overrideChanges["create"].append(override)

    # Find all overrides in Unbound that don't exist in Netbox to stage for deletion
    netboxAddresses = {nbAddress["address"].split("/")[0] for nbAddress in nbAddresses}
    overridesNotInNetbox = [entry for entry in opnsenseOverrides if entry["server"] not in netboxAddresses]
    for override in overridesNotInNetbox:
        overrideChanges["delete"].append(override)
    
    # Evaluate all staged changes
    print("Change Summary")
    for action in [{"name": "Creations", "slug":"create"}, {"name": "Updates", "slug": "update"}, {"name": "Deletions", "slug": "delete"}, {"name": "No action", "slug": "none"}]:
        print("\t" + action["name"] + ": " + str(len(overrideChanges[action["slug"]])))
        if action["slug"] == "none":
            continue
        for item in overrideChanges[action["slug"]]:
            print("\t\t---\n\t\tHostname: " + item["hostname"] + "\n\t\tIP Address: " + item["server"] + "\n\t\tDescription: " + item["description"])

    for override in overrideChanges["create"]:
        print(opnsense.createUnboundHostOverride(override))
    for override in overrideChanges["update"]:
        print(opnsense.updateUnboundHostOverride(override))
    for override in overrideChanges["delete"]:
        print(opnsense.deleteUnboundHostOverride(override))
    print(opnsense.applyUnboundChanges())

if __name__ == "__main__":
    main()
