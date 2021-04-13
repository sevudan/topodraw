#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telnetlib
import time
import paramiko

from abc import ABC, abstractmethod
from connection.HostCheck import CheckHost


class ConnectionError(Exception):
    """Connection exception"""


class Connection(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send_cmd(self, cmd):
        pass

    @abstractmethod
    def send_cmd_shell(self, cmd):
        pass

    @abstractmethod
    def close(self):
        pass

class SSHStrategy(Connection):

    def __init__(self, hostname, username, password, port):
        self.client = paramiko.SSHClient()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
            )
            print("Host '{}' connecting via SSH.".format(self.hostname))
        except paramiko.AuthenticationException:
            print("Host '{}' authentication fail.".format(self.hostname))

    def send_cmd(self, cmd):
        try:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            data = stdout.read() + stderr.read()
            return data.decode("utf-8")
        except Exception as err:
            print(err)

    def send_cmd_shell(self, cmd):
        comm = self.client.invoke_shell()
        comm.send(cmd)
        time.sleep(2)
        output = comm.recv(65535)
        output = output.decode("utf-8")
        return output

    def close(self):
        self.client.close()
        print("Host '{}' the SSH session closed.\n".format(self.hostname))


class TelnetStrategy(Connection):

    def __init__(self, hostname, username, password=None, port=None):
        self.tn = telnetlib.Telnet(hostname)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        try:
            self.tn.expect([b"login: ", b"sername: "], 5)
            self.tn.write(self.username.encode("ascii") + b"\n")
            self.tn.read_until(b"assword:")
            self.tn.write(self.password.encode("ascii") + b"\n")
            self.tn.expect([b"#", b">"], 5)
            print("Host '{}' connecting via telnet.".format(self.hostname))
        except Exception as err:
            print(err)

    def send_cmd(self, cmd):
        try:
            self.tn = telnetlib.Telnet(self.hostname, self.port)
            self.tn.write(self.password.encode("ascii") + b"\n")
            self.tn.expect([b"#", b">"], 5)
            print("Host '{}' connecting via telnet.".format(self.hostname))
        except Exception as err:
            print(err)

    def send_cmd_shell(self, cmd):
        for cmd in cmd.split('\n'):
            cmd = cmd + '\n'
            self.tn.write(cmd.encode("utf-8"))
        time.sleep(3)
        output = self.tn.read_very_eager().decode("utf-8")
        return output

    def close(self):
        self.tn.close()
        print("Host '{}' telnet session closed.\n".format(self.hostname))


class Connect:
    def connect_to_host(self,  shell=False, **access) -> Connection:
        hostname = access["hostname"]
        username = access["username"]
        password = access["password"]
        check = CheckHost()
        port_status = False
        if check.is_host_alive(hostname):
                print("Host '{}' is alive".format(hostname))
                for port in [22, 23]:
                    port_open = check.is_open_port(hostname, port)
                    if port_open:
                        port_status = True
                        try:
                            if shell and port == 22:
                                connection = SSHStrategy(hostname, username, password, port)
                                connection.connect()
                                return connection
                            if port == 22:
                                connection = SSHStrategy(hostname, username, password, port)
                                connection.connect()
                                return connection
                            if port == 23:
                                connection = TelnetStrategy(hostname, username, password, port)
                                connection.connect()
                                return connection
                        except Exception as err:
                            print(err)
                    else:
                        print("Host '{}' hasn't open port {}.".format(hostname, port))
                if port_status is False:
                    raise ConnectionError("Host '{}' hasn't open ports.\n".format(hostname))
        else:
            raise ConnectionError("Host {} unreachable\n".format(hostname))