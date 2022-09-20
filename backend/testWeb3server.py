from eth_typing import abi
from web3 import Web3
import json

# abi_file_path = os.path.join(
#     os.getcwd(), '../token/build/contracts/JoideaCoin.json')


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

accounts = w3.eth.accounts

contract.functions.checkBalance(
    accounts[0], accounts[1]).transact({'from': accounts[1]})

# contract.functions.sendTokenToClient(
#     w3.toWei(20, 'ether')).transact({'from': accounts[1]})

contract.functions.checkBalance(
    accounts[0], accounts[1]).transact({'from': accounts[1]})
# print(contract)
# print(contract.functions)

# contract.functions.testEvent().transact({'from': accounts[1]})
print(contract.functions.getAdmin().call())


# print(admin, ' is admin')
# print(accounts)
# print('event fired')

# print(w3.fromWei(contract.functions.balanceOf(
#     accounts[0]).call(), 'ether'))
# print(w3.fromWei(contract.functions.balanceOf(
#     accounts[1]).call(), 'ether'))

print('event')


# tbl = w3.eth.get_balance(fisrt_acc)
# print(w3.isConnected())
# # print(w3.eth.get_block('latest'))
# print(w3.fromWei(tbl, 'ether'))
