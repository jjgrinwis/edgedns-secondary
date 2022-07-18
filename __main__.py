"""A Python Pulumi program to create some secondary zones in EdgeDNS"""

import pulumi
import pulumi_akamai as akamai
import csv

# before using Pulumi, make sure you have the correct API permissions on the Akamai platform
# https://developer.akamai.com/api/getting-started#permission
# https://www.pulumi.com/docs/intro/cloud-providers/akamai/setup/
#
# in our example we're going to store our group_name in our Pulumi stack
# each project can have different stacks so select correct stack when starting pulumi
# for this demo using our training environment
# $ pulumi config set akamai:dnsSection gss_training
# $ pulumi config set group_name "GSS Training Internal-C-1IE2OHM New Name"
config = pulumi.Config()
group_name = config.require("group_name")

# lookup contract and group id
contract_id = akamai.get_contracts().contracts[0].contract_id
group_id = akamai.get_group(contract_id=contract_id, group_name=group_name).id

# now read a file with all the zones we need to create
# first line in CSV has the field names used as dict keys per row
# zone;masters;tsig_name;tsig_algorithm;tsig_secret
with open("zones.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        # each row will have a zone and list of masters and possible tsig values
        # now let's create these secondary zones using akamai.DnsZone resource
        # https://www.pulumi.com/registry/packages/akamai/api-docs/edgedns/dnszone/
        # masters should be list of IPs!

        # we're creating a dict and feed that into akamai.DnsZone call
        DnsZoneArgs = {}
        DnsZoneArgs["contract"] = contract_id
        DnsZoneArgs["group"] = group_id
        DnsZoneArgs["zone"] = row["zone"]
        DnsZoneArgs["masters"] = row["masters"].split(",")
        DnsZoneArgs["comment"] = "created via Pulumi"
        DnsZoneArgs["type"] = "secondary"

        # tsig is optional, only add tsig to dict if needed.
        # DictReader will set it to None if it's empty so don't add it if None
        if row["tsig_name"] is not None:
            DnsZoneArgs["tsig_key"] = {}
            DnsZoneArgs["tsig_key"]["name"] = row["tsig_name"]
            DnsZoneArgs["tsig_key"]["secret"] = row["tsig_secret"]
            DnsZoneArgs["tsig_key"]["algorithm"] = row["tsig_algorithm"]

        # pass our created dict as argument to DnsZone
        my_zone = akamai.DnsZone(row["zone"], **DnsZoneArgs)
