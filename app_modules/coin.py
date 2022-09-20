from subprocess import call
from eth_typing import abi
from web3 import Web3
from eth_account import account
from web3.contract import check_for_forbidden_api_filter_arguments
import json


class Coin:
    def __init__(
        self, contract_addr, abi_path, coin_name, network_addr="http://192.168.0.2:8545"
    ) -> None:
        f = open(abi_path)
        abi_data = json.load(f)["abi"]
        f.close()
        self.w3 = Web3(Web3.HTTPProvider(network_addr))

        self.name = coin_name

        self.contract = self.w3.eth.contract(
            address=contract_addr, abi=abi_data)

    def getBalance(self, wallet_address):
        return self.w3.fromWei(
            self.contract.functions.balanceOf(wallet_address).call(), "ether"
        )

    def sendTokenFromClient(self, wallet_address, amount):
        self.contract.functions.sendTokenFromClient(
            self.w3.toWei(amount, "ether")
        ).transact({"from": wallet_address})

    def sendTokenToClient(self, wallet_address, amount):
        self.contract.functions.sendTokenToClient(
            self.w3.toWei(amount, "ether")
        ).transact({"from": wallet_address})

    def getLatestBlock(self):
        return self.w3.eth.get_block('latest')

    def getTrasactionData(self, functionName:str, *params):
        args = []
        for i in params:
            args.append(i)
        print(args)
        call_data = self.contract.encodeABI(functionName, args=args)
        return call_data
