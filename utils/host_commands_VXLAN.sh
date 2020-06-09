#!/bin/bash

#Host 1: ip 192.168.213.10

sudo ip link add vxlan0 type vxlan id 40 remote 192.168.213.11 local 192.168.213.10 dev eth0 port 0 0
sudo ifconfig vxlan0 up

cd mininet/examples
sudo python domain.py

sh ovs-vsctl add-port s1 vxlan0 -- set interface vxlan0 type=vxlan option:remote_ip=192.168.213.11 option:key=flow ofport_request=10


#Host 1: ip 192.168.213.10
sudo ip link add vxlan0 type vxlan id 40 remote 192.168.213.10 local 192.168.213.11 dev eth0 port 0 0
sudo ifconfig vxlan0 up

cd mininet/examples
sudo python domain.py

sh ovs-vsctl add-port s1 vxlan0 -- set interface vxlan0 type=vxlan option:remote_ip=192.168.213.10 option:key=flow ofport_request=10


#### IN HOST 1
h1 ping 10.0.0.3

#### IN HOST2
h1 ping 10.0.0.1
