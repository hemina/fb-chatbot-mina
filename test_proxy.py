
import json, urllib




proxy_http = 'http://proxy-bru.adroot.local:8080'
proxy_https = 'https://proxy-bru.adroot.local:8080'

proxies =  {'http': proxy_http, 'https': proxy_https}
opener = urllib.FancyURLopener(proxies)

f = opener.open('http://bnp-ip-onecms-api.bearstech.com/push/fundsearchv2/PV_FR-IND/FRE')
print f.read()


