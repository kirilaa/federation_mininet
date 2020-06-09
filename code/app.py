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
web3= Web3(Web3.WebsocketProvider("ws://10.5.1.73:7545"))

abi_path = "../contracts/build/contracts/"

print('Coinbase account: ',web3.eth.coinbase)
print('\nAccounts: ',web3.eth.accounts)

with open(abi_path+"Federation.json") as c_json:
    contract_json = json.load(c_json)

contract_abi = contract_json["abi"]
contract_address = Web3.toChecksumAddress('0x1B46f5d28afcB389936625c5CD2b451f1D12A3f2')

Federation_contract = web3.eth.contract(abi= contract_abi, address = contract_address)

coinbase = web3.eth.coinbase

print("Etherbase:", coinbase)

# tx_hash = Federation_contract.functions.addOperator(Web3.toBytes(text='AD1'), 2).transact({'from': coinbase})
info, location = Federation_contract.functions.getOperatorInfo(web3.eth.coinbase).call()

print("\n\n",web3.toText(info), web3.toInt(location))

print("\n\tAnnounce service ------>\n")

# new_service = Federation_contract.functions.AnnounceService(_requirements= 100,_location = [2], _id = web3.toBytes(text = 'service1')).transact({'from':coinbase})
new_service_anouncement = Federation_contract.functions.GetServiceAnnounce(_id = web3.toBytes(text= 'service1'), _creator = coinbase).call()
print(web3.toText(text = new_service_anouncement[0]))
print("\n",new_service_anouncement)
event_filter = Federation_contract.events.ServiceAnnouncement.createFilter(fromBlock='0x0')


print("\nEVENTS:\n")
print(event_filter)
for event in event_filter.get_all_entries():
    print(event)