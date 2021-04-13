#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Topology:
    """
    Build list with IGP data from protocol OSPF. Example parameter:
    ['0.0.0.0', 'Router', '10.255.0.1', 'Transit', '10.0.12.2', '200']

    :return list of tuple.
    """

    def get_ospf_igp_data(self, data: list) -> list:
        topology = []
        for raw in data:
            area = raw[0]
            lsa = raw[1]
            if lsa == "Router":
                rid = raw[2]
                linktype = raw[3]
                if (linktype == "Transit"
                        or linktype == "TransNet"
                        or linktype == "PointToPoint"
                        or linktype == "P-2-P"):

                    network = raw[4]
                    if network == 0:
                        continue
                    metric = raw[5]
                    topology.append({"area": area, "rid": rid, "hostname": "None",
                                     "local_ip": network, "src_metric": metric})
                else:
                    continue
        result = self.get_links(topology)
        return result

    # Finde
    # Функция возвращает список , содержащий
    # пару маршрутизаторов, сеть и метрику для этого линка.
    def get_links(self, topology: list) -> list:
        networks = list(set([net["local_ip"] for net in topology]))
        result = []
        for link in networks:
            local = []
            for node in topology:
                net = node["local_ip"]
                if link == net:
                    local.append(node)
            result.append(tuple(local))
        return result

    """
    Find ABR Routers in data from protocols OSPF and ISIS.
    :return list.
    """

    def get_abr_nodes(self, data: list) -> list:
        result = []
        for raw in data:
            abr_flag = raw[1]
            abr_flag = abr_flag.lower()
            # Find ABR router. For protocol OSPF value must equal "Summury".
            # For protocol ISIS value must equal '0x3' or 'l1l2'.
            if abr_flag == "summary" or abr_flag == "0x3" \
                    or abr_flag == "l1l2":
                result.append(raw[2])
        result = list(set(result))
        return result

    """
    Find Node in igp Area.        
    :return dictionary.
    """

    def get_area_scope_nodes(self, topology: list) -> dict:
        area_scope = {}
        area = ""
        for raw in topology:
            local = raw[0]
            rid = raw[1]
            if area == "" or area != local:
                area_scope[local] = []
                area_scope[local].append(rid)
                area = local
            else:
                area_scope[local].append(rid)
                for k in area_scope.keys():
                    result = list(set(area_scope[k]))
                    area_scope[k] = result
        return area_scope

    def active_routing_protocols(self, protocols: list) -> list:
        if protocols.__len__() == 0:
            return list()
        active_protocols = []
        for proto in protocols:
            # For Juniper cli.
            if proto.__len__() == 1:
                active_protocols.append(proto[0])
            # For Nokia cli.
            if proto.__len__() == 2:
                if proto[1].lower() == "up" or proto[1].lower() == "active":
                    active_protocols.append(proto[0])
        return active_protocols

    def get_isis_router_hostname(self, data) -> dict:
        result = {}
        for line in data:
            rid = line[2]
            hostname = line[5]
            result[hostname] = rid
        return result

    def get_isis_igp_data(self, data: list) -> list:
        hostname = self.get_isis_router_hostname(data)
        data_length = data.__len__()
        start_slice = 3
        idx = 0
        topology = []
        while idx < data_length:
            start_line = data[idx]
            start_line = start_line[start_slice:start_line.__len__()]
            first_set_raw = set(start_line)
            next_raw = data[idx + 1:data_length]
            for line in next_raw:
                # Get slice with ip address connection and hostname
                # example: ['10.0.45.1', '10', 'dr04', 'dr05', '10.0.45.2']
                line = line[start_slice:line.__len__()]
                second_set_raw = set(line)
                if first_set_raw == second_set_raw:
                    # overlap.append(next_raw)
                    # Add metric to the end of the line.
                    data[idx].append(line[1])
                    topology.append(data[idx])
                    break
            idx = idx + 1
        result = []
        for line in topology:
            rid = hostname[line[6]]
            line.insert(7, rid)
            result.append(tuple([{"area": line[0], "level": line[1],
                                  "rid": line[2], "local_ip": line[3],
                                  "src_metric": line[4], "hostname": line[5]},
                                 {"hostname": line[6], "rid": line[7],
                                  "tgt_ip": line[8], "tgt_metric": line[9]}
                                 ]))
        return result
