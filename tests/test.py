from pathlib import Path

import textfsm

from builder.BuildTopology import Topology
from builder.Parser import Parser, Router

s = """A:r02# show router isis 1 database detail 

===============================================================================
Router Base ISIS Instance 1 Database
===============================================================================

Displaying Level 1 database
-------------------------------------------------------------------------------
Level (1) LSP Count : 0

Displaying Level 2 database
-------------------------------------------------------------------------------
LSP ID    : r01.00-00                                   Level     : L2  
Sequence  : 0x5                    Checksum  : 0xa194   Lifetime  : 3085
Version   : 1                      Pkt Type  : 20       Pkt Ver   : 1
Attributes: L1L2                   Max Area  : 3        
SysID Len : 6                      Used Len  : 138      Alloc Len : 138
 
TLVs : 
  Area Addresses:
    Area Address : (3) 49.0001
  Supp Protocols:
    Protocols     : IPv4
  IS-Hostname   : r01                 
  Router ID   :
    Router ID   : 10.255.0.1
  I/F Addresses :
    I/F Address   : 10.255.0.1
    I/F Address   : 10.0.12.1
    I/F Address   : 10.0.13.1
  TE IS Nbrs   :
    Nbr   : r03.00                              
    Default Metric  : 10
    Sub TLV Len     : 12
    IF Addr   : 10.0.13.1
    Nbr IP    : 10.0.13.2
  TE IS Nbrs   :
    Nbr   : r02.00                              
    Default Metric  : 10
    Sub TLV Len     : 12
    IF Addr   : 10.0.12.1
    Nbr IP    : 10.0.12.2
  TE IP Reach   :
    Default Metric  : 10
    Control Info:    , prefLen 24
    Prefix   : 10.0.12.0
    Default Metric  : 10              
    Control Info:    , prefLen 24
    Prefix   : 10.0.13.0
    Default Metric  : 0
    Control Info:    , prefLen 32
    Prefix   : 10.255.0.1

-------------------------------------------------------------------------------
LSP ID    : r02.00-00                                   Level     : L2  
Sequence  : 0x3                    Checksum  : 0x57d1   Lifetime  : 3043
Version   : 1                      Pkt Type  : 20       Pkt Ver   : 1
Attributes: L1L2                   Max Area  : 3        
SysID Len : 6                      Used Len  : 162      Alloc Len : 1492
 
TLVs : 
  Area Addresses:
    Area Address : (3) 49.0001
  Supp Protocols:
    Protocols     : IPv4
  IS-Hostname   : r02
  Router ID   :
    Router ID   : 10.255.0.2
  I/F Addresses :
    I/F Address   : 10.0.21.1         
    I/F Address   : 10.0.23.1
    I/F Address   : 10.255.0.2
    I/F Address   : 10.0.12.2
    I/F Address   : 10.0.24.2
  TE IS Nbrs   :
    Nbr   : r03.00                              
    Default Metric  : 10
    Sub TLV Len     : 12
    IF Addr   : 10.0.23.1
    Nbr IP    : 10.0.23.2
  TE IS Nbrs   :
    Nbr   : r01.00                              
    Default Metric  : 10
    Sub TLV Len     : 12
    IF Addr   : 10.0.12.2
    Nbr IP    : 10.0.12.1
  TE IP Reach   :
    Default Metric  : 10
    Control Info:    , prefLen 24
    Prefix   : 10.0.12.0
    Default Metric  : 10
    Control Info:    , prefLen 24
    Prefix   : 10.0.21.0              
    Default Metric  : 10
    Control Info:    , prefLen 24
    Prefix   : 10.0.23.0
    Default Metric  : 10
    Control Info:    , prefLen 24
    Prefix   : 10.0.24.0
    Default Metric  : 0
    Control Info:    , prefLen 32
    Prefix   : 10.255.0.2

-------------------------------------------------------------------------------
LSP ID    : r03.00-00                                   Level     : L2  
Sequence  : 0x5                    Checksum  : 0x22dd   Lifetime  : 3033
Version   : 1                      Pkt Type  : 20       Pkt Ver   : 1
Attributes: L1L2                   Max Area  : 3        
SysID Len : 6                      Used Len  : 138      Alloc Len : 138
 
TLVs : 
  Area Addresses:
    Area Address : (3) 49.0001
  Supp Protocols:
    Protocols     : IPv4
  IS-Hostname   : r03                 
  Router ID   :
    Router ID   : 10.255.0.3
  I/F Addresses :
    I/F Address   : 10.0.13.2
    I/F Address   : 10.0.23.2
    I/F Address   : 10.255.0.3
  TE IS Nbrs   :
    Nbr   : r01.00                              
    Default Metric  : 10
    Sub TLV Len     : 12
    IF Addr   : 10.0.13.2
    Nbr IP    : 10.0.13.1
  TE IS Nbrs   :
    Nbr   : r02.00                              
    Default Metric  : 10
    Sub TLV Len     : 12
    IF Addr   : 10.0.23.2
    Nbr IP    : 10.0.23.1
  TE IP Reach   :
    Default Metric  : 10
    Control Info:    , prefLen 24
    Prefix   : 10.0.13.0
    Default Metric  : 10              
    Control Info:    , prefLen 24
    Prefix   : 10.0.23.0
    Default Metric  : 0
    Control Info:    , prefLen 32
    Prefix   : 10.255.0.3
 
"""
string2 = """admin@vMX-1> show isis database extensive 
IS-IS level 1 link-state database:
vMX-1.00-00 Sequence: 0x5, Checksum: 0x4c04, Lifetime: 3182 secs
   IS neighbor: r02.00                        Metric:       10
     Two-way fragment: r02.00-00, Two-way first fragment: r02.00-00
   IP prefix: 10.0.21.0/24                    Metric:       10 Internal Up
   IP prefix: 10.255.0.7/32                   Metric:        0 Internal Up
   IP prefix: 192.168.56.0/24                 Metric:       10 Internal Up

  Header: LSP ID: vMX-1.00-00, Length: 122 bytes
    Allocated length: 1000 bytes, Router ID: 10.255.0.7
    Remaining lifetime: 3182 secs, Level: 1, Interface: 0
    Estimated free bytes: 824, Actual free bytes: 878
    Aging timer expires in: 3182 secs
    Protocols: IP, IPv6

  Packet: LSP ID: vMX-1.00-00, Length: 122 bytes, Lifetime : 3198 secs
    Checksum: 0x4c04, Sequence: 0x5, Attributes: 0x1 <L1>
    NLPID: 0x83, Fixed length: 27 bytes, Version: 1, Sysid length: 0 bytes
    Packet type: 18, Packet version: 1, Max area: 0

  TLVs:
    Area address: 49.0001 (3)
    LSP Buffer Size: 1000               
    Speaks: IP
    Speaks: IPV6
    IP router id: 10.255.0.7
    IP address: 10.255.0.7
    Hostname: vMX-1
    IS extended neighbor: r02.00, Metric: default 10
      IP address: 10.0.21.2
      Neighbor's IP address: 10.0.21.1
      Local interface index: 330, Remote interface index: 0
    IP extended prefix: 10.0.21.0/24 metric 10 up
    IP extended prefix: 192.168.56.0/24 metric 10 up
    IP extended prefix: 10.255.0.7/32 metric 0 up
  No queued transmissions

r02.00-00 Sequence: 0x5, Checksum: 0xc72a, Lifetime: 3177 secs
   IS neighbor: vMX-1.00                      Metric:       10
     Two-way fragment: vMX-1.00-00, Two-way first fragment: vMX-1.00-00
   IS neighbor: dr04.00                       Metric:       10
     Two-way fragment: dr04.00-00, Two-way first fragment: dr04.00-00
   IP prefix: 10.0.21.0/24                    Metric:       10 Internal Up
   IP prefix: 10.0.24.0/24                    Metric:       10 Internal Up
   IP prefix: 10.255.0.2/32                   Metric:        0 Internal Up
                                        
  Header: LSP ID: r02.00-00, Length: 138 bytes
    Allocated length: 284 bytes, Router ID: 10.255.0.2
    Remaining lifetime: 3177 secs, Level: 1, Interface: 330
    Estimated free bytes: 146, Actual free bytes: 146
    Aging timer expires in: 3177 secs
    Protocols: IP

  Packet: LSP ID: r02.00-00, Length: 138 bytes, Lifetime : 3200 secs
    Checksum: 0xc72a, Sequence: 0x5, Attributes: 0x3 <L1 L2>
    NLPID: 0x83, Fixed length: 27 bytes, Version: 1, Sysid length: 0 bytes
    Packet type: 18, Packet version: 1, Max area: 3

  TLVs:
    Area address: 49.0001 (3)
    Speaks: IP
    Hostname: r02
    IP router id: 10.255.0.2
    IP address: 10.0.21.1
    IP address: 10.255.0.2
    IP address: 10.0.24.2
    IS extended neighbor: vMX-1.00, Metric: default 10
      IP address: 10.0.21.1
      Neighbor's IP address: 10.0.21.2  
    IS extended neighbor: dr04.00, Metric: default 10
      IP address: 10.0.24.2
      Neighbor's IP address: 10.0.24.1
    IP extended prefix: 10.0.21.0/24 metric 10 up
    IP extended prefix: 10.0.24.0/24 metric 10 up
    IP extended prefix: 10.255.0.2/32 metric 0 up
  No queued transmissions

dr05.00-00 Sequence: 0x5, Checksum: 0xcc4b, Lifetime: 3177 secs
   IS neighbor: dr04.00                       Metric:       10
     Two-way fragment: dr04.00-00, Two-way first fragment: dr04.00-00
   IP prefix: 10.0.45.0/24                    Metric:       10 Internal Up
   IP prefix: 10.255.0.5/32                   Metric:        0 Internal Up

  Header: LSP ID: dr05.00-00, Length: 142 bytes
    Allocated length: 284 bytes, Router ID: 10.255.0.5
    Remaining lifetime: 3177 secs, Level: 1, Interface: 330
    Estimated free bytes: 142, Actual free bytes: 142
    Aging timer expires in: 3177 secs
    Protocols: IP

  Packet: LSP ID: dr05.00-00, Length: 142 bytes, Lifetime : 3200 secs
    Checksum: 0xcc4b, Sequence: 0x5, Attributes: 0x1 <L1>
    NLPID: 0x83, Fixed length: 27 bytes, Version: 1, Sysid length: 0 bytes
    Packet type: 18, Packet version: 1, Max area: 3

  TLVs:
    Area address: 49.0001 (3)
    Speaks: IP
    Hostname: dr05
    IP router id: 10.255.0.5
    IS neighbor: dr04.00, Internal, Metric: default 10
    IP prefix: 10.0.45.0/24, Internal, Metric: default 10, Up
    IP prefix: 10.255.0.5/32, Internal, Metric: default 0, Up
    IP address: 10.0.45.2
    IP address: 10.255.0.5
    IS extended neighbor: dr04.00, Metric: default 10
      IP address: 10.0.45.2
      Neighbor's IP address: 10.0.45.1
    IP extended prefix: 10.0.45.0/24 metric 10 up
    IP extended prefix: 10.255.0.5/32 metric 0 up
  No queued transmissions

dr04.00-00 Sequence: 0x6, Checksum: 0x4883, Lifetime: 3177 secs
   IS neighbor: r02.00                        Metric:       10
     Two-way fragment: r02.00-00, Two-way first fragment: r02.00-00
   IS neighbor: dr05.00                       Metric:       10
     Two-way fragment: dr05.00-00, Two-way first fragment: dr05.00-00
   IP prefix: 10.0.24.0/24                    Metric:       10 Internal Up
   IP prefix: 10.0.45.0/24                    Metric:       10 Internal Up
   IP prefix: 10.255.0.4/32                   Metric:        0 Internal Up

  Header: LSP ID: dr04.00-00, Length: 139 bytes
    Allocated length: 284 bytes, Router ID: 10.255.4.4
    Remaining lifetime: 3177 secs, Level: 1, Interface: 330
    Estimated free bytes: 145, Actual free bytes: 145
    Aging timer expires in: 3177 secs
    Protocols: IP

  Packet: LSP ID: dr04.00-00, Length: 139 bytes, Lifetime : 3200 secs
    Checksum: 0x4883, Sequence: 0x6, Attributes: 0x1 <L1>
    NLPID: 0x83, Fixed length: 27 bytes, Version: 1, Sysid length: 0 bytes
    Packet type: 18, Packet version: 1, Max area: 3

  TLVs:
    Area address: 49.0001 (3)
    Speaks: IP
    Hostname: dr04
    IP router id: 10.255.4.4            
    IP address: 10.0.24.1
    IP address: 10.0.45.1
    IP address: 10.255.0.4
    IS extended neighbor: r02.00, Metric: default 10
      IP address: 10.0.24.1
      Neighbor's IP address: 10.0.24.2
    IS extended neighbor: dr05.00, Metric: default 10
      IP address: 10.0.45.1
      Neighbor's IP address: 10.0.45.2
    IP extended prefix: 10.0.24.0/24 metric 10 up
    IP extended prefix: 10.0.45.0/24 metric 10 up
    IP extended prefix: 10.255.0.4/32 metric 0 up
  No queued transmissions

IS-IS level 2 link-state database:
"""

string3 = """OSPF database, Area 0.0.0.0
  Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   10.255.0.1       10.255.0.1       0x80000008  1381  0x2  0xe003  60
  bits 0x0, link count 3
  id 10.0.13.2, data 10.0.13.1, Type Transit (2)
    Topology count: 0, Default metric: 100
  id 10.0.12.2, data 10.0.12.1, Type Transit (2)
    Topology count: 0, Default metric: 100
  id 10.255.0.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  Topology default (ID 0)
    Type: Transit, Node ID: 10.0.12.2
      Metric: 200, Bidirectional
    Type: Transit, Node ID: 10.0.13.2
      Metric: 100, Bidirectional
  Aging timer 00:36:58
  Installed 00:22:59 ago, expires in 00:36:59
  Last changed 01:00:29 ago, Change count: 3
Router   10.255.0.2       10.255.0.2       0x8000000a  1380  0x2  0x41d3  72
  bits 0x0, link count 4
  id 10.0.12.2, data 10.0.12.2, Type Transit (2)
    Topology count: 0, Default metric: 100
  id 10.0.23.2, data 10.0.23.1, Type Transit (2)
    Topology count: 0, Default metric: 100
  id 10.255.0.2, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  Topology default (ID 0)
    Type: Transit, Node ID: 10.0.23.2
      Metric: 100, Bidirectional
    Type: Transit, Node ID: 10.0.12.2   
      Metric: 100, Bidirectional
  Aging timer 00:36:59
  Installed 00:22:59 ago, expires in 00:37:00
  Last changed 01:00:29 ago, Change count: 3
Router   10.255.0.3       10.255.0.3       0x80000008  1379  0x2  0x299c  60
  bits 0x0, link count 3
  id 10.0.13.2, data 10.0.13.2, Type Transit (2)
    Topology count: 0, Default metric: 100
  id 10.0.23.2, data 10.0.23.2, Type Transit (2)
    Topology count: 0, Default metric: 100
  id 10.255.0.3, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  Topology default (ID 0)
    Type: Transit, Node ID: 10.0.23.2
      Metric: 100, Bidirectional
    Type: Transit, Node ID: 10.0.13.2
      Metric: 100, Bidirectional
  Aging timer 00:37:00
  Installed 00:22:57 ago, expires in 00:37:01
  Last changed 01:00:27 ago, Change count: 3
"""
"""
template2 = Path.cwd().resolve().joinpath('templates/nokia')
template2 = template2.joinpath("isis_db.template")
template = DIR_TEMPLATE = Path.cwd().resolve().joinpath('templates/juniper/ospf_db.template')
print(template)

def parse_data(template, string) -> list:
    #print(string)
    template = open(template)
    re_table = textfsm.TextFSM(template)
    parse_data = re_table.ParseText(string)
    for raw in parse_data:
        print(raw)


parse_data(template2, s)"""

alu = """environment no more 
A:r02# show system information 

===============================================================================
System Information
===============================================================================
System Name            : r02
System Type            : 7750 SR-12
Chassis Topology       : Standalone
System Version         : B-13.0.R1
System Contact         : 
System Location        : 
System Coordinates     : 
System Active Slot     : A
System Up Time         : 0 days, 00:23:20.59 (hr:min:sec)
 
SNMP Port              : 161
SNMP Engine ID         : 0000197f00007066ff000000
SNMP Engine Boots      : 156
SNMP Max Message Size  : 1500
SNMP Admin State       : Enabled
SNMP Oper State        : Enabled
SNMP Index Boot Status : Not Persistent
SNMP Sync State        : N/A
 
Tel/Tel6/SSH/FTP Admin : Enabled/Disabled/Disabled/Enabled
Tel/Tel6/SSH/FTP Oper  : Up/Down/Down/Up
 
BOF Source             : cf3:
Image Source           : primary
Config Source          : primary
Last Booted Config File: cf3:\config.cfg
Last Boot Cfg Version  : MON FEB 08 10:30:49 2021 UTC
Last Boot Config Header: # TiMOS-B-13.0.R1 both/i386 ALCATEL SR 7750
                         Copyright (c) 2000-2015 Alcatel-Lucent. # All rights
                         reserved. All use subject to applicable license
                         agreements. # Built on Fri Feb 27 21:10:57 PST 2015
                         by builder in /rel13.0/b1/R1/panos/main # Generated
                         MON FEB 08 10:30:49 2021 UTC
Last Boot Index Version: N/A
Last Boot Index Header : # TiMOS-B-13.0.R1 both/i386 ALCATEL SR 7750
                         Copyright (c) 2000-2015 Alcatel-Lucent. # All rights
                         reserved. All use subject to applicable license
                         agreements. # Built on Fri Feb 27 21:10:57 PST 2015
                         by builder in /rel13.0/b1/R1/panos/main # Generated
                         MON FEB 08 10:30:49 2021 UTC
Last Saved Config      : N/A
Time Last Saved        : N/A
Changes Since Last Save: No
Max Cfg/BOF Backup Rev : 5
Cfg-OK Script          : N/A
Cfg-OK Script Status   : not used
Cfg-Fail Script        : N/A
Cfg-Fail Script Status : not used
 
Management IP Addr     : 192.168.56.102/24
Primary DNS Server     : N/A
Secondary DNS Server   : N/A
Tertiary DNS Server    : N/A
DNS Domain             : (Not Specified)
DNS Resolve Preference : ipv4-only
DNSSEC AD Validation   : False
DNSSEC Response Control: drop
BOF Static Routes      : None
ATM Location ID        : 01:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
ATM OAM Retry Up       : 2
ATM OAM Retry Down     : 4
ATM OAM Loopback Period: 10
 
ICMP Vendor Enhancement: Disabled
Eth QinQ untagged SAP  : False
EFM OAM Grace Tx Enable: False
===============================================================================
A:r02# show router status 

===============================================================================
Router Status (Router: Base)
===============================================================================
                         Admin State                        Oper State
-------------------------------------------------------------------------------
Router                   Up                                 Up
OSPFv2-0                 Up                                 Up
RIP                      Not configured                     Not configured
RIP-NG                   Not configured                     Not configured
ISIS-0                   Up                                 Up
ISIS-1                   Down                               Down
MPLS                     Up                                 Up
RSVP                     Down                               Down
LDP                      Up                                 Up
BGP                      Up                                 Up
IGMP                     Not configured                     Not configured
MLD                      Not configured                     Not configured
PIM                      Not configured                     Not configured
PIMv4                    Not configured                     Not configured
OSPFv3                   Not configured                     Not configured
MSDP                     Not configured                     Not configured
 
Max IPv4 Routes          No Limit                            
Max IPv6 Routes          No Limit                            
Total IPv4 Routes        8                                   
Total IPv6 Routes        0                                   
Max Multicast Routes     No Limit                            
Total IPv4 Mcast Routes  PIM not configured                  
ECMP Max Routes          1                                   
Weighted ECMP            Disabled                            
Mcast Info Policy        default                             
Triggered Policies       No                                  
LDP Shortcut             Disabled                            
Single SFM Overload      Disabled                            
IP Fast Reroute          Disabled                            
Reassembly ISA-BB group  Not configured                     
Ipv6 Nbr Reachab. time   Not configured                     30
===============================================================================
A:r02# show router ospf 0 neighbor | match Neighbors 
No. of Neighbors: 4
A:r02# show router ospf 0 database detail 

===============================================================================
OSPFv2 (0) Link State Database (Type : All) (Detailed)
===============================================================================
-------------------------------------------------------------------------------
Router LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.1
Link State Id    : 10.255.0.1 (184483841)
LSA Type         : Router               
Sequence No      : 0x8000000f           Checksum         : 0xd20a
Age              : 1295                 Length           : 60
Options          : E                    
Flags            : None                 Link Count       : 3
Link Type (1)    : Transit Network      
DR Rtr Id (1)    : 10.0.13.2            I/F Address (1)  : 10.0.13.1
No of TOS (1)    : 0                    Metric-0 (1)     : 100
Link Type (2)    : Transit Network      
DR Rtr Id (2)    : 10.0.12.2            I/F Address (2)  : 10.0.12.1
No of TOS (2)    : 0                    Metric-0 (2)     : 100
Link Type (3)    : Stub Network         
Network (3)      : 10.255.0.1           Mask (3)         : 255.255.255.255
No of TOS (3)    : 0                    Metric-0 (3)     : 0
-------------------------------------------------------------------------------
Router LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.2 (184483842)
LSA Type         : Router               
Sequence No      : 0x80000010           Checksum         : 0x38d5
Age              : 1300                 Length           : 72
Options          : E                    
Flags            : ABR                  Link Count       : 4
Link Type (1)    : Transit Network      
DR Rtr Id (1)    : 10.0.12.2            I/F Address (1)  : 10.0.12.2
No of TOS (1)    : 0                    Metric-0 (1)     : 100
Link Type (2)    : Transit Network      
DR Rtr Id (2)    : 10.0.23.2            I/F Address (2)  : 10.0.23.1
No of TOS (2)    : 0                    Metric-0 (2)     : 100
Link Type (3)    : Transit Network      
DR Rtr Id (3)    : 10.0.21.2            I/F Address (3)  : 10.0.21.1
No of TOS (3)    : 0                    Metric-0 (3)     : 100
Link Type (4)    : Stub Network         
Network (4)      : 10.255.0.2           Mask (4)         : 255.255.255.255
No of TOS (4)    : 0                    Metric-0 (4)     : 0
-------------------------------------------------------------------------------
Router LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.3
Link State Id    : 10.255.0.3 (184483843)
LSA Type         : Router               
Sequence No      : 0x8000000d           Checksum         : 0x1fa1
Age              : 1298                 Length           : 60
Options          : E                    
Flags            : None                 Link Count       : 3
Link Type (1)    : Transit Network      
DR Rtr Id (1)    : 10.0.13.2            I/F Address (1)  : 10.0.13.2
No of TOS (1)    : 0                    Metric-0 (1)     : 100
Link Type (2)    : Transit Network      
DR Rtr Id (2)    : 10.0.23.2            I/F Address (2)  : 10.0.23.2
No of TOS (2)    : 0                    Metric-0 (2)     : 100
Link Type (3)    : Stub Network         
Network (3)      : 10.255.0.3           Mask (3)         : 255.255.255.255
No of TOS (3)    : 0                    Metric-0 (3)     : 0
-------------------------------------------------------------------------------
Router LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.7
Link State Id    : 10.255.0.7 (184483847)
LSA Type         : Router               
Sequence No      : 0x80000006           Checksum         : 0xae45
Age              : 1341                 Length           : 60
Options          : E DC                 
Flags            : ASBR                 Link Count       : 3
Link Type (1)    : Transit Network      
DR Rtr Id (1)    : 10.0.21.2            I/F Address (1)  : 10.0.21.2
No of TOS (1)    : 0                    Metric-0 (1)     : 1
Link Type (2)    : Stub Network         
Network (2)      : 192.168.56.0         Mask (2)         : 255.255.255.0
No of TOS (2)    : 0                    Metric-0 (2)     : 1
Link Type (3)    : Stub Network         
Network (3)      : 10.255.0.7           Mask (3)         : 255.255.255.255
No of TOS (3)    : 0                    Metric-0 (3)     : 0
-------------------------------------------------------------------------------
Network LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.12.2 (167775234)
LSA Type         : Network              
Sequence No      : 0x80000001           Checksum         : 0xd648
Age              : 1304                 Length           : 32
Options          : E                    
Network Mask     : 255.255.255.0        No of Adj Rtrs   : 2
Router Id (1)    : 10.255.0.2           Router Id (2)    : 10.255.0.1
-------------------------------------------------------------------------------
Network LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.3
Link State Id    : 10.0.13.2 (167775490)
LSA Type         : Network              
Sequence No      : 0x80000003           Checksum         : 0xcb4e
Age              : 1304                 Length           : 32
Options          : E                    
Network Mask     : 255.255.255.0        No of Adj Rtrs   : 2
Router Id (1)    : 10.255.0.3           Router Id (2)    : 10.255.0.1
-------------------------------------------------------------------------------
Network LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.3
Link State Id    : 10.0.23.2 (167778050)
LSA Type         : Network              
Sequence No      : 0x80000003           Checksum         : 0x6ba3
Age              : 1305                 Length           : 32
Options          : E                    
Network Mask     : 255.255.255.0        No of Adj Rtrs   : 2
Router Id (1)    : 10.255.0.3           Router Id (2)    : 10.255.0.2
-------------------------------------------------------------------------------
Network LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.7
Link State Id    : 10.0.21.2 (167777538)
LSA Type         : Network              
Sequence No      : 0x80000001           Checksum         : 0xb337
Age              : 1341                 Length           : 32
Options          : E DC                 
Network Mask     : 255.255.255.0        No of Adj Rtrs   : 2
Router Id (1)    : 10.255.0.7           Router Id (2)    : 10.255.0.2
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.24.0 (167778304)
LSA Type         : Summary              
Sequence No      : 0x80000005           Checksum         : 0x5d69
Age              : 1296                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.45.0 (167783680)
LSA Type         : Summary              
Sequence No      : 0x80000001           Checksum         : 0x69e7
Age              : 1296                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 200
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.0
-------------------------------------------------------------------------------
Area Id          : 0.0.0.0              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.4 (184483844)
LSA Type         : Summary              
Sequence No      : 0x80000001           Checksum         : 0x4698
Age              : 1296                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.255      Metric-0         : 100
-------------------------------------------------------------------------------
Router LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.2 (184483842)
LSA Type         : Router               
Sequence No      : 0x80000005           Checksum         : 0xb5d5
Age              : 1299                 Length           : 36
Options          : E                    
Flags            : ABR                  Link Count       : 1
Link Type (1)    : Transit Network      
DR Rtr Id (1)    : 10.0.24.1            I/F Address (1)  : 10.0.24.2
No of TOS (1)    : 0                    Metric-0 (1)     : 100
-------------------------------------------------------------------------------
Router LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.4
Link State Id    : 10.255.0.4 (184483844)
LSA Type         : Router               
Sequence No      : 0x80000007           Checksum         : 0x7a43
Age              : 1300                 Length           : 60
Options          : E                    
Flags            : None                 Link Count       : 3
Link Type (1)    : Transit Network      
DR Rtr Id (1)    : 10.0.24.1            I/F Address (1)  : 10.0.24.1
No of TOS (1)    : 0                    Metric-0 (1)     : 100
Link Type (2)    : Stub Network         
Network (2)      : 10.0.45.0            Mask (2)         : 255.255.255.0
No of TOS (2)    : 0                    Metric-0 (2)     : 100
Link Type (3)    : Stub Network         
Network (3)      : 10.255.0.4           Mask (3)         : 255.255.255.255
No of TOS (3)    : 0                    Metric-0 (3)     : 0
-------------------------------------------------------------------------------
Network LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.4
Link State Id    : 10.0.24.1 (167778305)
LSA Type         : Network              
Sequence No      : 0x80000001           Checksum         : 0x729c
Age              : 1300                 Length           : 32
Options          : E                    
Network Mask     : 255.255.255.0        No of Adj Rtrs   : 2
Router Id (1)    : 10.255.0.4           Router Id (2)    : 10.255.0.2
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.12.0 (167775232)
LSA Type         : Summary              
Sequence No      : 0x80000002           Checksum         : 0xe7ed
Age              : 1300                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.13.0 (167775488)
LSA Type         : Summary              
Sequence No      : 0x80000002           Checksum         : 0xc8a7
Age              : 1288                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 200
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.21.0 (167777536)
LSA Type         : Summary              
Sequence No      : 0x80000002           Checksum         : 0x8448
Age              : 1337                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.0.23.0 (167778048)
LSA Type         : Summary              
Sequence No      : 0x80000002           Checksum         : 0x6e5c
Age              : 1296                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.1 (184483841)
LSA Type         : Summary              
Sequence No      : 0x80000001           Checksum         : 0x647d
Age              : 1300                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.255      Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.2 (184483842)
LSA Type         : Summary              
Sequence No      : 0x80000002           Checksum         : 0x6cd7
Age              : 1338                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.255      Metric-0         : 0
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.3 (184483843)
LSA Type         : Summary              
Sequence No      : 0x80000001           Checksum         : 0x508f
Age              : 1296                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.255      Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.7 (184483847)
LSA Type         : Summary              
Sequence No      : 0x80000001           Checksum         : 0x28b3
Age              : 1339                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.255      Metric-0         : 100
-------------------------------------------------------------------------------
Summary LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 192.168.56.0 (3232249856)
LSA Type         : Summary              
Sequence No      : 0x80000001           Checksum         : 0xde6b
Age              : 1339                 Length           : 28
Options          : E                    
Network Mask     : 255.255.255.0        Metric-0         : 101
-------------------------------------------------------------------------------
AS Summ LSA for Area 0.0.0.1
-------------------------------------------------------------------------------
Area Id          : 0.0.0.1              Adv Router Id    : 10.255.0.2
Link State Id    : 10.255.0.7 (184483847)
LSA Type         : AS Summ              
Sequence No      : 0x80000001           Checksum         : 0x1ac0
Age              : 1339                 Length           : 28
Options          : E                    
Network Mask     : N/A                  Metric-0         : 100
-------------------------------------------------------------------------------
AS Ext LSA for Network 0.0.0.0 (0)
-------------------------------------------------------------------------------
Area Id          : N/A                  Adv Router Id    : 10.255.0.7
Link State Id    : 0.0.0.0 (0)
LSA Type         : AS Ext               
Sequence No      : 0x80000003           Checksum         : 0x7827
Age              : 877                  Length           : 36
Options          : E DC                 
Network Mask     : 0.0.0.0              Fwding Address   : 0.0.0.0
Metric Type      : Type 2               Metric-0         : 0
Ext Route Tag    : 0x0                  
===============================================================================
A:r02# show router isis 1 adjacency | match Adjacencies 
A:r02# show router isis 1 database detail 

===============================================================================
Router Base ISIS Instance 1 Database
===============================================================================

Displaying Level 1 database
-------------------------------------------------------------------------------
Level (1) LSP Count : 0

Displaying Level 2 database
-------------------------------------------------------------------------------
Level (2) LSP Count : 0
===============================================================================
A:r02# environment more 
A:r02# 
A:r02# 
"""
hu = """
<R2>display ospf lsdb router 

	 OSPF Process 1 with Router ID 10.0.2.2
		         Area: 0.0.0.0
		 Link State Database 


  Type      : Router
  Ls id     : 10.0.3.3
  Adv rtr   : 10.0.3.3  
  Ls age    : 207 
  Len       : 60 
  Options   :  ABR  E  
  seq#      : 80000007 
  chksum    : 0xb5ad
  Link count: 3
   * Link ID: 10.0.3.0     
     Data   : 255.255.255.0 
     Link Type: StubNet      
     Metric : 0 
     Priority : Low
   * Link ID: 10.0.2.2     
     Data   : 10.0.23.3    
     Link Type: P-2-P        
     Metric : 4882
   * Link ID: 10.0.23.0    
     Data   : 255.255.255.0 
     Link Type: StubNet      
     Metric : 4882 
     Priority : Low

  Type      : Router
  Ls id     : 10.0.2.2
  Adv rtr   : 10.0.2.2  
  Ls age    : 203 
  Len       : 60 
  Options   :  ABR  E  
  seq#      : 80000007 
  chksum    : 0xdf87
  Link count: 3
   * Link ID: 10.0.2.0     
     Data   : 255.255.255.0 
     Link Type: StubNet      
     Metric : 0 
     Priority : Low
   * Link ID: 10.0.3.3     
     Data   : 10.0.23.2    
     Link Type: P-2-P        
     Metric : 4882
   * Link ID: 10.0.23.0    
     Data   : 255.255.255.0 
     Link Type: StubNet      
     Metric : 4882 
     Priority : Low
		         Area: 0.0.0.2
		 Link State Database 


  Type      : Router
  Ls id     : 10.0.4.4
  Adv rtr   : 10.0.4.4  
  Ls age    : 184 
  Len       : 48 
  Options   :  ASBR  E  
  seq#      : 80000008 
  chksum    : 0x4d9c
  Link count: 2
   * Link ID: 10.0.124.4   
     Data   : 10.0.124.4   
     Link Type: TransNet     
     Metric : 10
   * Link ID: 10.0.4.0     
     Data   : 255.255.255.0 
     Link Type: StubNet      
     Metric : 0 
     Priority : Low
"""

count = """
<Test>display ospf cumulative

	 OSPF Process 1 with Router ID 10.0.2.2
		 Cumulations

  IO Statistics
             Type        Input     Output
            Hello           53        122
   DB Description            2          3
   Link-State Req            1          1
Link-State Update            3          3
   Link-State Ack            2          2
  ASE: (Disabled)
  LSAs originated by this router

  Router: 2
  Network: 0
  Sum-Net: 4
  Sum-Asbr: 0
  External: 0
  NSSA: 0
  Opq-Link: 0
  Opq-Area: 0
  Opq-As: 0
  LSAs Originated: 6  LSAs Received: 3

  Routing Table:
    Intra Area: 2  Inter Area: 0  ASE: 0

  Up Interface Cumulate: 1

      Neighbor Cumulate:
  =======================================================

      Neighbor cumulative data. (Process 1)
  -------------------------------------------------------
  Down:       0 Init:        0 Attempt:    0 2-Way:    0
  Exstart:    0 Exchange:    0 Loading:    0 Full:     0
  Retransmit Count: 0

      Neighbor cumulative data. (Total)
  -------------------------------------------------------
  Down:       0 Init:        0 Attempt:    0 2-Way:    0
  Exstart:    0 Exchange:    0 Loading:    0 Full:     0
  Retransmit Count: 0"""

template = Path.cwd().resolve().joinpath('../templates/huawei/ospf_status.template')
p = Parser()
pd = p.parse_data(template, count)

for i in pd:
    print(i)

"""
b = BuildTopology()
result = b.get_ospf_igp_data(pd)


router = Router("1.1.1.1", "Nokia", alu)
router.igp_adjacency("ospf")

p = Parser()
pd = p.parse_data(template, string3)

b = BuildTopology()
result = b.get_ospf_igp_data(pd)

for i in result:
    print(i)"""


