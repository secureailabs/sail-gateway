import redis
from dnslib import QTYPE, RCODE, RR, A, DNSError, DNSRecord
from dnslib.server import BaseResolver, DNSServer

# Hardcoded DNS resolutions in a dictionary
dns_records = {
    "example.com.": "172.20.100.11",
    "test.com.": "192.0.2.2"
}

redis_instance = redis.Redis(host='localhost', port=6379, decode_responses=True)

class HardcodedResolver(BaseResolver):
    def resolve(self, request: DNSRecord, handler):
        reply = request.reply()
        qname = request.q.qname

        # Check if the domain is in the database
        domain = redis_instance.get(str(qname))
        if domain:
            reply.add_answer(RR(rname=qname, rtype=QTYPE.A, rdata=A(domain), ttl=60))
        else:
            reply.header.rcode = RCODE.NXDOMAIN

        return reply

if __name__ == "__main__":
    # Add the dns_records to the database
    for domain, ip in dns_records.items():
        redis_instance.set(domain, ip)

    resolver = HardcodedResolver()
    server = DNSServer(resolver, port=53, address="0.0.0.0")
    print("Starting DNS server on port 53...")
    server.start()
