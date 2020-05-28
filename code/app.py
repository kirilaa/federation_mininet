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
web3= Web3(Web3.HTTPProvider("http://163.117.140.242:7545"))

print('Coinbase account: ',web3.eth.coinbase)
print('\nAccounts: ',web3.eth.accounts)