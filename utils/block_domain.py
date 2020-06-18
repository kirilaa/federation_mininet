#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
import random
import sys
import os
import json
import time
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
from web3.providers.rpc import HTTPProvider

from web3 import Web3
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import Intf
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os
import time
import argparse


parser = argparse.ArgumentParser(description='Initialize domain with network')
parser.add_argument('--domain', type=str, default='consumer|provider',
                        help='Flag for the consumer or provider domain.\nUse "consumer" for consumer domain, "provider" for provider domain')

#                        help='CSV path where results are stored')
args = parser.parse_args()
print(args.domain)

# Configure the web3 interface to the Blockchain and SC
web3= Web3(Web3.WebsocketProvider("ws://10.5.1.73:7545"))
abi_path = "./contracts/"
with open(abi_path+"Federation.json") as c_json:
   contract_json = json.load(c_json)

contract_abi = contract_json["abi"]
contract_address = Web3.toChecksumAddress('0x30AB1A2b567874722d4335A5bf1034772B3c95A0')
Federation_contract = web3.eth.contract(abi= contract_abi, address = contract_address)
coinbase = web3.eth.coinbase
eth_address = web3.eth.accounts

#Configure CONSUMER variables
timestamp = int(time.time())
service_id = ''
service_endpoint_consumer = ''
service_consumer_address = ''
service_requirements = 'ip=10.0.0.4'

#Conifgure PROVIDER variables
service_endpoint_provider = ''
federated_host = ''
service_price = 0
bid_index = 0
winner = coinbase

#Configure the IP address
stream = os.popen('ip a | grep 192.168.213').read()
stream = stream.split('inet ',1)
ip_address = stream[1].split('/',1)
ipaddress = ip_address[0]

#Configure the domain variables
domain_registered = True
domain = args.domain
if domain == 'consumer':
   #block_address = eth_address[1]
   block_address = coinbase
   timestamp = int(time.time())
   service_id = 'service'+str(timestamp)
   service_endpoint_consumer = ipaddress
   service_consumer_address = block_address
else:
   block_address = eth_address[2]
   #block_address = coinbase
   service_endpoint_provider = ipaddress
   service_id = ''

def Web3_code():
    coinbase = web3.eth.coinbase
    eth_address = web3.eth.accounts

    print("Etherbase:", coinbase)
    print("IP address:", ipaddress)
    print("Federation contract:\n", Federation_contract.functions);

def RegisterDomain(domain_registered):
    if domain_registered == False:
        tx_hash = Federation_contract.functions.addOperator(Web3.toBytes(text='AD2')).transact({'from': block_address})
        domain_registered = True
        print("Domain has been registered")
    else:
        print("Domain already registered")

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    if domain == 'consumer':
        h1 = net.addHost( 'h1', ip='10.0.0.1' )
        h2 = net.addHost( 'h2', ip='10.0.0.2' )
    else:
        h1 = net.addHost( 'h1', ip='10.0.0.3' )
        h2 = net.addHost( 'h2', ip='10.0.0.4' )

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )
    #stream = os.popen('sudo ip link add vxlan0 type vxlan id 40 remote 192.168.213.10 local 192.168.213.11 dev eth0 port 0 0')
    #stream = os.popen('sudo ifconfig vxlan0 up')
    #Intf( 'vxlan0', node=s1 )    

    info( '*** Creating links\n' )
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    return net

def startNet(net):
    info( '*** Starting network\n')
    net.start()

    #info( '*** Running CLI\n' )
    #"""CLI( net )"""
    #time.sleep(5)
    #info( '*** Stopping network' )
    #net.stop()

def federateNet(serviceDeployedInfo, net):
    "Create an empty network and add nodes to it."
    #net = Mininet( controller=Controller )
    #info( '*** Adding controller\n' )
    #net.addController( 'c0' )
    #info( '*** Adding hosts\n' )
    #h1 = net.addHost( 'h1', ip='10.0.0.3' )
    #h2 = net.addHost( 'h2', ip='10.0.0.4' )
    #info( '*** Adding switch\n' )
    #s1 = net.addSwitch( 's1' )
    stopNet(net)
    net= emptyNet()
    s1 = net.getNodeByName('s1')
    #serviceDeployedInfo = '192.168.213.11'
    vxlan_string = 'sudo ip link add vxlan0 type vxlan id 40 remote ' + serviceDeployedInfo + ' local ' + ipaddress + ' dev eth0 port 0 0'
    #stream = os.popen('sudo ip link add vxlan0 type vxlan id 40 remote 192.168.213.10 local 192.168.213.11 dev eth0 port 0 0')
    print(vxlan_string)
    stream = os.popen(vxlan_string)
    #time.sleep(2)
    stream = os.popen('sudo ifconfig vxlan0 up')
    time.sleep(2)
    Intf( 'vxlan0', node=s1 )

    #info( '*** Creating links\n' )
    #net.addLink( h1, s1 )
    #net.addLink( h2, s1 )

    #info( '*** Starting network\n')
    net.start()
    return net
    #info( '*** Running CLI\n' )
    #"""CLI( net )"""
    #time.sleep(5)
    #info( '*** Stopping network' )
    #net.stop()

def stopNet(net):
    info( '*** Stopping network' )
    net.stop()

def AnnounceService():
    new_service = Federation_contract.functions.AnnounceService(_requirements= web3.toBytes(text = service_requirements), _endpoint_consumer= web3.toBytes(text = service_endpoint_consumer), _id = web3.toBytes(text = service_id)).transact({'from':block_address})
    block = web3.eth.getBlock('latest')
    blocknumber = block['number']
    #event_filter = Federation_contract.events.NewBid.createFilter(fromBlock=web3.toHex(blocknumber), argument_filters={'_id':web3.toBytes(text= service_id)})
    event_filter = Federation_contract.events.NewBid.createFilter(fromBlock=web3.toHex(blocknumber))
    return event_filter

def GetBidInfo(bid_index):
    bid_info = Federation_contract.functions.GetBid(_id= web3.toBytes(text= service_id), bider_index= bid_index, _creator=block_address).call()
    return bid_info

def ChooseProvider(bid_index):
    chosen_provider = Federation_contract.functions.ChooseProvider(_id= web3.toBytes(text= service_id), bider_index= bid_index).transact({'from':block_address})

def GetServiceState(serviceid):
    service_state = Federation_contract.functions.GetServiceState(_id = web3.toBytes(text= serviceid)).call()
    #print("Service State: ",service_state)
    return service_state

def GetDeployedInfo():
    service_endpoint_provider = '192.168.213.11'
    return service_endpoint_provider

def ServiceAnnouncementEvent():
    block = web3.eth.getBlock('latest')
    blocknumber = block['number']
    print("\nLatest block:",blocknumber)
    event_filter = Federation_contract.events.ServiceAnnouncement.createFilter(fromBlock=web3.toHex(blocknumber))
    return event_filter

def PlaceBid(service_id):
    service_price = 5
    Federation_contract.functions.PlaceBid(_id= web3.toBytes(text= service_id), _price= service_price, _endpoint= web3.toBytes(text= service_endpoint_provider)).transact({'from':block_address})
    block = web3.eth.getBlock('latest')
    blocknumber = block['number']
    print("\nLatest block:",blocknumber)
    event_filter = Federation_contract.events.ServiceAnnouncementClosed.createFilter(fromBlock=web3.toHex(blocknumber))
    return event_filter

def CheckWinner(service_id):
    state = GetServiceState(service_id)
    result = False
    if state == 1:
        result = Federation_contract.functions.isWinner(_id= web3.toBytes(text= service_id), _winner= block_address).call()
        print("Am I a Winner? ", result)
    return result

def DeployService(net):
    stopNet(net)
    net= emptyNet()
    s1 = net.getNodeByName('s1')
    serviceDeployedInfo = '192.168.213.12'
    vxlan_string = 'sudo ip link add vxlan0 type vxlan id 40 remote ' + serviceDeployedInfo + ' local ' + ipaddress + ' dev eth0 port 0 0'
    #stream = os.popen('sudo ip link add vxlan0 type vxlan id 40 remote 192.168.213.10 local 192.168.213.11 dev eth0 port 0 0')
    print(vxlan_string)
    stream = os.popen(vxlan_string)
    #time.sleep(2)
    stream = os.popen('sudo ifconfig vxlan0 up')
    time.sleep(2)
    Intf( 'vxlan0', node=s1 )

    #info( '*** Creating links\n' )
    #net.addLink( h1, s1 )
    #net.addLink( h2, s1 )

    #info( '*** Starting network\n')
    net.start()
    return net

def ServiceDeployed(service_id):
    result = Federation_contract.functions.ServiceDeployed(info= web3.toBytes(text= ipaddress), _id= web3.toBytes(text= service_id)).transact({'from':block_address})

if __name__ == '__main__':
    setLogLevel( 'info' )
    Web3_code()
    RegisterDomain(domain_registered)
    net = emptyNet()
    startNet(net)
    if domain == 'consumer':
        print("\nSERVICE_ID:",service_id)
        debug_txt = input("\nCreate Service anouncement....(ENTER)")
        bids_event = AnnounceService()
        bidderArrived = False
        while bidderArrived == False:
            new_events = bids_event.get_all_entries()
            for event in new_events:
                event_id = str(web3.toText(event['args']['_id']))
                print(service_id, web3.toText(event['args']['_id']), event['args']['max_bid_index'])
                #if event_id == web3.toText(text= service_id):
                print("ENTERED")
                bid_index = int(event['args']['max_bid_index'])
                bidderArrived = True
                if int(bid_index) < 2:
                    bid_info = GetBidInfo(int(bid_index-1))
                    print(bid_info)
                    ChooseProvider(int(bid_index)-1)
                    break
        serviceDeployed = False
        while serviceDeployed == False:
            serviceDeployed = True if GetServiceState(service_id) == 2 else False
        serviceDeployedInfo = GetDeployedInfo()
        net = federateNet(serviceDeployedInfo, net)
        CLI(net)
        stopNet(net)

    if domain == 'provider':
        service_id = ''
        print("\nSERVICE_ID:",service_id)
        debug_txt = input("\nStart listening for federation events....(ENTER)")
        newService_event = ServiceAnnouncementEvent()
        newService = False
        open_services = []
        while newService == False:
            new_events = newService_event.get_all_entries()
            for event in new_events:
                service_id = web3.toText(event['args']['id'])
                if GetServiceState(service_id) == 0:
                    open_services.append(service_id)
            print("OPEN = ", len(open_services))
            if len(open_services) > 0:
                newService = True
        service_id = open_services[-1]
        winnerChosen_event = PlaceBid(service_id)
        winnerChosen = False
        while winnerChosen == False:
            new_events = winnerChosen_event.get_all_entries()
            for event in new_events:
                event_serviceid = web3.toText(event['args']['_id'])
                if event_serviceid == service_id:
                    winnerChosen = True
                    break
        am_i_winner = CheckWinner(service_id)
        if am_i_winner == True:
            net = DeployService(net)
            ServiceDeployed(service_id)
            CLI(net)
            #while True:
             #   print("Federated service deployed")
             #   time.sleep(10)
        else:
            print("I am not a Winner")
        stopNet(net)
    #time.sleep(5)
    #stopNet(net)
