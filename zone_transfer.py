import dns.zone
import dns.query
import dns.rdatatype

try:
    z = dns.zone.from_xfr(dns.query.xfr('10.129.2.193', 'inlanefreight.htb'))
    ns_count = 0
    for name, node in z.nodes.items():
        for rdataset in node.rdatasets:
            if rdataset.rdtype == dns.rdatatype.NS:
                ns_count += len(rdataset)
    print(ns_count)
except Exception as e:
    print(f"Error: {e}")