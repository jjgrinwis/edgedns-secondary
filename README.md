# edgedns-secondary
Add some secondary zones to Akamai EdgeDNS using Pulumi

Just create a zones.csv with the following fields
```
zone;masters;tsig_name;tsig_algorithm;tsig_secret
pulumi1.nl;1.2.3.4,5.6.7.8;testing-xfer;hmac-sha256;base64key
pulumi2.nl;5.6.7.8,9.7.6.5,4.6.8.0
```
Just create a new [Pulumi Python](https://www.pulumi.com/docs/intro/languages/python/), make sure to setup the correct [Akamai API credentials](https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials) and a ```pulumi up``` will do the work for you.
