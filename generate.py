#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import yaml

from builder.Commands import *
from builder.BuildConfig import BuildConfig
from builder.Parser import Parser, Router, Node
from connection.HostConnect import Connect
# logging.basicConfig(level=logging.DEBUG)


class Generate:

    def node_vendor(self, connection):
        start_cmd = ".\n.\n"
        output = connection.send_cmd_shell(start_cmd)
        parser = Parser()
        return parser.get_vendor(output)

    def get_router_info(self, connect, topology, exclude=None, **access) -> list:
        routers = []
        if type(topology[0]) is tuple:
            for raw in topology:
                for router in raw:
                    routers.append(router["rid"])
        routers = list(set(routers))
        if exclude.__len__() > 0:
            routers = list(set(routers) ^ set(exclude))
        nodes = []
        for rid in routers:
            access["hostname"] = rid
            try:
                connection = connect.connect_to_host(**access, invoke_shell=True)
            except Exception as err:
                print(err)
                continue
            vendor = self.node_vendor(connection)
            cmd = ""
            if vendor == "Juniper":
                cmd = Juniper.get_command()
            elif vendor == "Nokia":
                cmd = Nokia.get_command()
            output = connection.send_cmd_shell(cmd)
            connection.close()
            node = Node(rid, vendor, output)
            nodes.append(node)
        return nodes

    def get_router(self, connect, protocol, **access):
        connection = connect.connect_to_host(**access, invoke_shell=True)
        vendor = self.node_vendor(connection)
        cmd = ""
        if vendor == "Juniper":
            cmd = Juniper.get_command()
        elif vendor == "Nokia":
            cmd = Nokia.get_command()
        output = connection.send_cmd_shell(cmd)
        connection.close()
        hostname = access["hostname"]
        return Router(hostname, vendor, output, protocol)

    def start(self):
        connect = Connect()
        igp_router = []
        abrs = []

        """
        hostname = "10.255.0.2"
        username = "admin"
        password = "admin123        
        access = {"hostname": hostname, "username": username, "password": password}
        """
        with open('app/config.yaml', mode='r') as file:
            access = yaml.load(file, Loader=yaml.FullLoader)
            print(access)
        protocol = access['igp']
        # Connect to first router and get igp database and ABRs.
        try:
            router = self.get_router(connect, protocol, **access)
        except Exception as err:
            print(str(err) + "First router error. Script aborted...")
            sys.exit(0)
        # Check igp adjansensy.
        if router.igp_adjacency():
            abrs.extend(router.get_abr_nodes())
            igp_router.append(router)
        else:
            raise Exception("IGP Protocol not running.\nScript aborted...")
        if abrs.__len__() > 0:
            igp_router.pop()
            for rid in abrs:
                access["hostname"] = rid
                try:
                    router = self.get_router(connect, protocol, **access)
                    igp_router.append(router)
                except Exception:
                    continue
        # Connecting to other nodes in topology for getting information.
        topology = []
        for router in igp_router:
            topology.extend(router.igp_topology())
        # Connect to other nodes in topology for geting information.
        other_nodes = self.get_router_info(connect, topology, abrs, **access)
        igp_router.extend(other_nodes)
        info = {}
        for router in igp_router:
            info[router.rid] = router.all_host_info()
        build = BuildConfig()
        build.build_js_topology_data(protocol, topology, info)


if __name__ == '__main__':
    try:
        run = Generate()
        run.start()
    except KeyboardInterrupt:
        sys.stdout.write('You pressed Ctrl+C!'
                         'Script aborted...')
        sys.exit(0)

        import napalm
