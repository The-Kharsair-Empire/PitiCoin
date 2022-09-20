from eth_typing import abi
from web3 import Web3
import json
import time


f = open('serverConfigs.json')
configs = json.load(f)
f.close()

contract_addr = configs['contract_addr']
server_addr = configs['server_addr']
abi_path = configs['abi_path']

f = open(abi_path)
abi_data = json.load(f)['abi']
f.close()

w3 = Web3(Web3.HTTPProvider(server_addr))

contract = w3.eth.contract(address=contract_addr, abi=abi_data)


def callback(event):
    print(event)


event_filter_1 = contract.events.eventFired.createFilter(fromBlock='latest')
event_filter_2 = contract.events.secondEvent.createFilter(fromBlock='latest')
event_filter_3 = contract.events.revealBalances.createFilter(
    fromBlock='latest')
event_filter_4 = contract.events.tokenTransferredToClient.createFilter(
    fromBlock='latest')

event_filters = []
event_filters.append(event_filter_1)
event_filters.append(event_filter_2)
event_filters.append(event_filter_3)
event_filters.append(event_filter_4)
# event_filter = w3.eth.filter({"address": contract_addr})

while True:
    for event_filter in event_filters:
        for event in event_filter.get_new_entries():
            callback(event)
    time.sleep(2)
