#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scapy.all import *
import scapy.layers.inet as inet


class CheckHost:

    def is_host_alive(self, host):
        timeout = 5
        conf.verb = 0
        packet = inet.IP(dst=host, ttl=20) / inet.ICMP()
        reply = sr1(packet, timeout=timeout)
        if reply is None:
            return False
        else:
            host_reach = reply.getlayer(inet.ICMP).type == 0
        return True if host_reach else False

    def is_open_port(self, host, port):
        #if self.scan_tcp_ports(host, port):
        #    return True
        if self.scan_xmas(host, port):
            return True
        return False

    def scan_tcp_ports(self, host, port):
        src_port = RandShort()
        dst_port = port
        timeout = 5

        tcp_rsp = sr1(inet.IP(dst=host)
                      / inet.TCP(sport=src_port, dport=dst_port,
                                 flags='S'), timeout=timeout)

        if tcp_rsp is None:
            return False
        elif tcp_rsp.haslayer(inet.TCP):
            if tcp_rsp.getlayer(inet.TCP).flags == 0x12:
                sr(inet.IP(dst=host) / inet.TCP(sport=src_port, dport=dst_port,
                                                flags="AR"), timeout=timeout)
                return True
            elif tcp_rsp.getlayer(inet.TCP).flags == 0x14:
                return False

    def scan_xmas(self, host, port):
        dst_port = port
        timeout = 10
        xmas_scan_resp = sr1(inet.IP(dst=host) / inet.TCP(dport=dst_port, flags="FPU"), timeout=timeout)

        if xmas_scan_resp is None:
            # Status Open|Filtered
            return True
        elif xmas_scan_resp.haslayer(inet.TCP):
            if (xmas_scan_resp.getlayer(inet.TCP).flags == 0x14):
                # Status Filtered
                return False
            elif xmas_scan_resp.haslayer(inet.ICMP):
                if xmas_scan_resp.getlayer(inet.ICMP).type == 3 \
                        and xmas_scan_resp.getlayer(inet.ICMP).code \
                        in [1, 2, 3, 9, 10, 13]:
                    # Status Filtered
                    return True