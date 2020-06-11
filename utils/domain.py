#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import Intf
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.3' )
    h2 = net.addHost( 'h2', ip='10.0.0.4' )

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )
    stream = os.popen('sudo ip link add vxlan0 type vxlan id 40 remote 192.168.213.10 local 192.168.213.11 dev eth0 port 0 0')
    stream = os.popen('sudo ifconfig vxlan0 up')
    Intf( 'vxlan0', node=s1 )

    info( '*** Creating links\n' )
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    """CLI( net )"""
    
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
