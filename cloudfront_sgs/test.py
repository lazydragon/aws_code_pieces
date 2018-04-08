import json
import urllib2

from netaddr import IPNetwork

def get_ip_groups_json(url):
    """
    Return the HTTP response from URL
    """
    print "Updating from " + url

    response = urllib2.urlopen(url)
    ip_json = response.read()

    return ip_json


def main():
    ip_ranges = json.loads(get_ip_groups_json('https://ip-ranges.amazonaws.com/ip-ranges.json'))
    cidrs = []
    for ip in ip_ranges['prefixes']:
        if ip['region'] == 'us-west-2' and ip['service'] != 'CLOUDFRONT':
            cidrs.append(ip['ip_prefix'])

    for cidr in cidrs:
        ips = IPNetwork(cidr)
        print """
        (
        (try_cast(split(request_ip, '.')[1] as bigint) * 256*256*256 
        + try_cast( split(request_ip , '.')[2] as bigint) * 256*256 
        + try_cast( split( request_ip, '.')[3] as bigint) * 256 
        + try_cast( split( request_ip, '.')[4] as bigint))
        <
        (try_cast(split('%s', '.')[1] as bigint) * 256*256*256 
        + try_cast( split( '%s', '.')[2] as bigint) * 256*256 
        + try_cast( split( '%s', '.')[3] as bigint) * 256 
        + try_cast( split( '%s', '.')[4] as bigint))
        and
        (try_cast(split(request_ip, '.')[1] as bigint) * 256*256*256 
        + try_cast( split(request_ip , '.')[2] as bigint) * 256*256 
        + try_cast( split( request_ip, '.')[3] as bigint) * 256 
        + try_cast( split( request_ip, '.')[4] as bigint))
        > 
        (try_cast(split('%s', '.')[1] as bigint) * 256*256*256 
        + try_cast( split( '%s', '.')[2] as bigint) * 256*256 
        + try_cast( split( '%s', '.')[3] as bigint) * 256 
        + try_cast( split( '%s', '.')[4] as bigint))
        ) or
        """ % (ips[-1],ips[-1],ips[-1],ips[-1], ips[0],ips[0],ips[0],ips[0])
        

if __name__ == "__main__":
    main()
