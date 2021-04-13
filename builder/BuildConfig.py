#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


class BuildConfig:

    def _node_info(self, nodes: list, info: dict) -> list:
        result = []
        routers = list(set([r["id"] for r in nodes]))
        for rid in routers:
            for node in nodes:
                try:
                    node_id = node["id"]
                except KeyError:
                    print("Node '{}' not found".format(rid))
                    continue
                if rid == node_id:
                    try:
                        local = info[rid]
                    except KeyError:
                        node["vendor"] = "None"
                        node["os_version"] = "None"
                        continue
                    node["vendor"] = local["vendor"]
                    node["os_version"] = local["os_version"]
                    result.append(node)
                    break
        return result
    
    """
    topology :argument List of Tuples
    """
    def _node(self, topology: list, info: dict) -> list:
        nodes = []
        if type(topology[0]) is tuple:
                for raw in topology:
                    for router in raw:
                        local = {}
                        local["id"] = router["rid"]
                        local["name"] = router["hostname"]
                        local["Lo"] = router["rid"]
                        nodes.append(local)
        result = self._node_info(nodes, info)
        return result

    def _ospf_links(self, topology) -> list:
        result = []
        idx = 0
        if type(topology[0]) is tuple:
            for raw in topology:
                local = {}
                raw_idx = list(range(0, raw.__len__()))
                for i in raw_idx:
                    router = raw[i]
                    if i == 0:
                        local["id"] = str(idx)
                        local["source"] = router["rid"]
                        local["area"] = router["area"]
                        local["src_network"] = router["local_ip"]
                        local["src_metric"] = router["src_metric"]
                    else:
                        local["target"] = router["rid"]
                        local["tgt_network"] = router["local_ip"]
                        local["tgt_metric"] = router["src_metric"]
                        local["color"] = "blue"
                result.append(local)
                idx = idx + 1
        return result

    def _isis_links(self, topology) -> list:
        result = []
        idx = 0
        if type(topology[0]) is tuple:
            for raw in topology:
                local = {}
                raw_idx = list(range(0, raw.__len__()))
                for i in raw_idx:
                    router = raw[i]
                    if i == 0:
                        local["id"] = str(idx)
                        local["source"] = router["rid"]
                        local["level"] = router["level"]
                        local["src_network"] = router["local_ip"]
                        local["src_metric"] = router["src_metric"]
                    else:
                        local["target"] = router["rid"]
                        local["tgt_network"] = router["tgt_ip"]
                        local["tgt_metric"] = router["tgt_metric"]
                        local["color"] = "blue"
                idx = idx + 1
                result.append(local)
        return result

    def _build_links(self, protocol, topology) -> list:
        if protocol == "ospf":
            return self._ospf_links(topology)
        if protocol == "isis":
            return self._isis_links(topology)

    def _build_node_set(self, builder, topology):
        template = "\'id\': \'{}\', \'nodes\': {}"
        area_scopes = builder.get_area_scope_nodes(topology)
        result = ""
        for k in area_scopes.keys():
            idx = k
            nodes = area_scopes[k]
            jstr = '{' + template.format(idx, nodes) + '}'
            result = jstr + ', ' + result
        result = list(result)[:result.__len__() - 2]
        return "".join(result)

    def build_js_topology_data(self, protocol: str, topology: list, nodeinfo: dict):
        DIR_UI = Path.cwd().resolve().joinpath('app/static/nextUI')

        if topology.__len__() == 0:
            raise Exception("Input topology data is Null\n")
        nodes = self._node(topology, nodeinfo)
        links = self._build_links(protocol, topology)
        result = {}
        result["nodes"] = nodes
        result["links"] = links
        json_obj = json.dumps(result)
        topology_data = "var topologyData = " + json_obj
        FILE_PATH = DIR_UI.joinpath("app/topology_data.js")
        with open(FILE_PATH, "w") as file:
            file.write(topology_data)
        sys.stdout.write("Build topology data DONE.\n")