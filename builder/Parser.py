#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import textfsm
import sys
import logging

from pathlib import Path
from builder.BuildTopology import Topology


class Parser:

    def is_nokia(self, string):
        string = string.lower()
        pattern = "(^(a|b):\+w>)|(^(a|b):.+#)"
        return bool(re.search(pattern, string))

    def is_cisco_ios(self, string):
        string = string.lower()
        pattern = "^\w+(>|#)"
        return bool(re.search(pattern, string))

    def is_huawei(self, string):
        string = string.lower()
        pattern = "(^\[.*\])|(^\<.*\>)"
        return bool(re.search(pattern, string))

    def is_junos(self, string):
        string = string.lower()
        pattern = "^\w.+@.*(>|#)"
        return bool(re.search(pattern, string))

    def parse_data(self, template, string) -> list:
        template = open(template)
        re_table = textfsm.TextFSM(template)
        parse_data = re_table.ParseText(string)
        return parse_data

    def node_version(self, pattern1, pattern2, string):
        hostname = re.search(pattern1, string)
        if hostname == None:
            hostname = "None"
        else:
            hostname = hostname.group(1)
        os = re.search(pattern2, string)
        if os == None:
            os = "None"
        else:
            os = os.group(1)
        return {"hostname": hostname, "os_version": os}

    def adjacency_count(self, pattern: str, string: str) -> int:
        count = re.search(pattern, string)
        return -1 if count is None else count.group(1)

    def get_vendor(self, string):
        try:
            string = string.split().pop()
        except AttributeError:
            sys.stdout.write("Error! Empty output. Vendor not recognized")
        return {self.is_nokia(string): "Nokia",
                self.is_cisco_ios(string): "Cisco",
                self.is_huawei(string): "Huawei",
                self.is_junos(string): "Juniper"}[True]


class Cli:

    def __init__(self):
        self.DIR_TEMPLATE = Path.cwd().resolve().joinpath('templates')
        self.build = Topology()
        self.parser = Parser()

    def is_file_exist(self, file) -> bool:
        if Path(file).is_file():
            return True
        else:
            sys.stdout.write("File {} dos not exist.\n".format(file))
            return False

    def get_parameters(self, igp) -> Path:
        templates = {"ospf": self.DIR_TEMPLATE.joinpath("ospf_db.template"),
                     "isis": self.DIR_TEMPLATE.joinpath("isis_db.template")}
        try:
            template = templates[igp]
            if self.is_file_exist(template):
                return template
        except KeyError:
            sys.stdout.write("Get template error! Raw for the protocol {} not found".format(igp))


class CliHuawei(Cli):

    def __init__(self):
        super().__init__()
        self.DIR_TEMPLATE = self.DIR_TEMPLATE.joinpath('huawei')

    def _clear_empty(self, line: list):
        return [string for string in line if string != '']

    def _hw_wrapper(self, data):
        idx = ''
        modules = []
        unit = []
        for line in data:
            name = line[0]
            unit_num = line[1]
            local_id = name + unit_num
            line = self._clear_empty(line[2:])
            local = [name, unit_num]
            if local_id == idx:
                unit.extend(line)
            else:
                idx = local_id
                unit = []
                unit.extend(local)
                unit.extend(line)
                modules.append(unit)
        return modules

    def get_hardware_info(self, output: str):
        template = self.DIR_TEMPLATE.joinpath("hw_info.template")
        data = self.parser.parse_data(template, output)
        modules = list(set([module[0] for module in data]))
        modules = {key: {} for key in modules}
        hardware = self._hw_wrapper(data)
        for unit in hardware:
            if unit.__len__() == 3:
                modules[unit[0]].update({unit[1]: {"PCB_version": unit[2]}})
            if unit.__len__() == 4:
                modules[unit[0]].update({unit[1]: {"Unit_version": unit[2],
                                           "PCB_version": unit[3]}})
            if unit[0] == "LPU":
                modules[unit[0]].update({unit[1]: {"LPU_version": unit[2],
                                                   "PCB_version": unit[3],
                                                   "NSE_version": unit[4],
                                                   unit[5]: {"PIC_version": unit[6],
                                                             "PCB_version": unit[7]}
                                                   }})
            if unit[0] == "POWER":
                local = {}
                line = unit[2:]
                for index, item in enumerate(line):
                    if index % 2 == 0:
                        local[item] = line[index + 1]
                modules[unit[0]].update({unit[1]: local})
        return modules

    def is_igp_adjacency(self, protocol: str, output: str):
        template = self.DIR_TEMPLATE.joinpath("ospf_status.template")
        if protocol == "isis":
            count = self.parser.parse_data(template, output)[0]
        else:
            count = self.parser.parse_data(template, output)[0]
        return True if count > 0 else False

    def get_hostname_version(self, output: str) -> dict:
        """
        pattern_hostname = "^<(\S+)>"
        pattern_os = "\n\w+\s\(\w\)\ssoftware.\sVersion\s(\S+\s\S+\s\S+)"
        return self.parser.node_version(pattern_hostname, pattern_os, string)"""
        template = self.DIR_TEMPLATE.joinpath("sh_version.template")
        facts = self.parser.parse_data(template, output)[0]
        result = {"hostname": facts[0], "software": facts[1],
                  "version": facts[2], "model": facts[3],
                  "uptime": facts[4]
                  }
        return result

    def get_active_protocols(self, output) -> list:
        template = self.DIR_TEMPLATE.joinpath("router_status.tmpl")
        if self.is_file_exist(template):
            protocols = self.parser.parse_data(template, output)
            return self.build.active_routing_protocols(protocols)


class CliJuniper(Cli):

    def __init__(self):
        super().__init__()
        self.DIR_TEMPLATE = self.DIR_TEMPLATE.joinpath('juniper')

    def is_igp_adjacency(self, protocol: str, output: str):
        if protocol == "isis":
            find_str = "show\sisis\sadjacency.+\\nCount:\s(\d+)"
        else:
            find_str = "show\sospf\sneighbor.+\\nCount:\s(\d+)"
        count = int(self.parser.adjacency_count(find_str, output))
        return True if count > 0 else False

    def get_hostname_version(self, string) -> dict:
        pattern_hostname = "\nHostname:\s(\w+.+)"
        pattern_os = "\nJunos:\s(\w+.+)"
        return self.parser.node_version(pattern_hostname, pattern_os, string)

    def get_active_protocols(self, output) -> list:
        template = self.DIR_TEMPLATE.joinpath("router_status.tmpl")
        if self.is_file_exist(template):
            protocols = self.parser.parse_data(template, output)
            return self.build.active_routing_protocols(protocols)


class CliNokia(Cli):

    def __init__(self):
        super().__init__()
        self.DIR_TEMPLATE = self.DIR_TEMPLATE.joinpath('nokia')

    def is_igp_adjacency(self, protocol: str, output: str):
        if protocol == "isis":
            find_str = "show\srouter\sisis\s\d\sadjacency\s\|\s\w+\s\w+\s+\\nAdjacencies\s:\s(\d+)"
        else:
            find_str = "show\srouter\sospf\s\d\sneighbor\s\|\smatch\s\w+\s+\\nNo\S\s\w+\sNeighbors:\s(\d+)"
        count = int(self.parser.adjacency_count(find_str, output))
        return True if count > 0 else False

    def get_hostname_version(self, string) -> dict:
        pattern_hostname = "\nSystem\sName\s+:\s(\w+.*)"
        pattern_os = "\nSystem\sVersion\s+:\s(\w+.*)"
        return self.parser.node_version(pattern_hostname, pattern_os, string)

    def get_active_protocols(self, output) -> list:
        template = self.DIR_TEMPLATE.joinpath("router_status.template")
        protocols = self.parser.parse_data(template, output)
        return self.build.active_routing_protocols(protocols)


class Node:

    cli_vendors = {"Juniper": CliJuniper(), "Nokia": CliNokia(),
                   "Huawei": CliHuawei()}

    def __init__(self, rid, vendor, output):
        if re.search("(\d+\.){3}\d+", rid) is None:
            raise ValueError("Incorrect RID. {}".format(rid))
        self.vendor = vendor
        self.rid = rid
        self.output = output
        try:
            self.cli = self.cli_vendors[vendor]
        except KeyError:
            sys.stdout.write("Error: Vendor not found!\n")

    def host_info(self) -> dict:
        result = self.cli.get_hostname_version(self.output)
        return result

    def hardware_info(self) -> dict:
        return  self.cli.get_hardware_info(self.output)

    def all_host_info(self) -> dict:
        result = self.host_info()
        result["vendor"] = self.vendor
        """hostname = result["hostname"]
        os = result["os_version"]"""
        return result

    def protocol_status(self) -> list:
        return self.cli.get_active_protocols(self.output)


class Router(Node):

    parser = Parser()
    build_topology = Topology()

    def __init__(self, rid, vendor, output, igp):
        super(Router, self).__init__(rid, vendor, output)
        self.igp = igp

    def __parse_igp_topology(self) -> list:
        template = self.cli.get_parameters(self.igp)
        return self.parser.parse_data(template, self.output)

    def igp_topology(self):
        parse_topology = self.__parse_igp_topology()
        if self.igp == "isis":
            return self.build_topology.get_isis_igp_data(parse_topology)
        else:
            return self.build_topology.get_ospf_igp_data(parse_topology)

    def get_abr_nodes(self) -> list:
        parse_topology = self.__parse_igp_topology()
        return self.build_topology.get_abr_nodes(parse_topology)

    def igp_adjacency(self):
        return self.cli.is_igp_adjacency(self.igp, self.output)