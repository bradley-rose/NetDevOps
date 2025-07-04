#!/bin/bash
# Install a crontab: 15 * * * * 	/mnt/netbox/scripts/dns.sh
source /opt/NetDevOps/Examples/Netbox-to-OPNsense-DNS/venv/bin/activate
cd /opt/NetDevOps/Examples/Netbox-to-OPNsense-DNS
output=$(python dns.py 2>&1)
# Only log if there are changes
if echo "$output" | grep -qE 'Creations: [1-9][0-9]*|Updates: [1-9][0-9]*|Deletions: [1-9][0-9]*'; then
    {
        echo "=== Script started at $(date) ==="
        echo "$output"
        echo "=== Script ended at $(date) ==="
    } >> /mnt/netbox/scripts/dnsRuntimeLogs.txt
fi
deactivate
cd ~
