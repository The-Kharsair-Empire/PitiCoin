from eth_typing import abi
from web3 import Web3
import json

f = open('serverConfigs.json')
configs = json.load(f)
f.close()

contract_addr = configs['contract_addr']
server_addr = configs['server_addr']
abi_path = configs['abi_path']

f = open(abi_path)
abi_data = json.load(f)['abi']
f.close()
admin = '0x6Ee4eb9CC37aff2Ce695CDb6162eA8a705af29B2'
account2 = '0x50Ff71D47e5347ed5db6CF126A6A409651c98C2b'

w3 = Web3(Web3.HTTPProvider(server_addr))

contract = w3.eth.contract(address=contract_addr, abi=abi_data)

bal = contract.functions.checkBalance(
    admin, account2).call()
print(bal)
print(w3.fromWei(contract.functions.balanceOf(
    account2).call(), 'ether'))
contract.functions.sendTokenToClient(
    w3.toWei(1, 'ether')).transact({'from': account2})
bal = contract.functions.checkBalance(
    admin, account2).call()

print(w3.fromWei(contract.functions.balanceOf(
    account2).call(), 'ether'))

print(bal)
