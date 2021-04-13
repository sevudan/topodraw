#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Command:
    pass


class Juniper(Command):

    @staticmethod
    def get_command():
        cmd = "show version | no-more\n" \
          "show ospf database extensive | no-more\n" \
          "show route table inet.0 protocol isis | no-more\n" \
          "show route table inet.0 protocol ospf | no-more\n" \
          "show ospf neighbor | count\n" \
          "show ospf database extensive | no-more\n" \
          "show isis adjacency | count\n" \
          "show isis database extensive | no-more\n"

        return cmd


class Nokia(Command):

    @staticmethod
    def get_command():
        cmd = "environment no more\n" \
          "show system information\n" \
          "show router status\n" \
          "show router ospf 0 neighbor | match Neighbors\n" \
          "show router ospf 0 database detail\n" \
          "show router isis 0 adjacency | match Adjacencies\n" \
          "show router isis 0 database detail\n" \
          "environment more\n"

        return cmd


class Huawei(Command):

    @staticmethod
    def get_command():
        cmd = "display version\n" \
              "display ospf peer\n" \
              "display ospf lsdb router\n" \
              "display ospf lsdb summary\n" \
              "display isis peer\n" \
              "display isis lsdb verbose\n"
        return cmd
