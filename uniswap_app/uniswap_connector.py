from subprocess import call
from eth_typing import abi
from web3 import Web3
from eth_account import account
from web3.contract import check_for_forbidden_api_filter_arguments
import json

# factory_addr='0x9c83dCE8CA20E9aAF9D3efc003b2ea62aBC08351' #v1
# factory_addr='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f' #v2
factory_addr='0x1F98431c8aD98523631AE4a59f267346ea31F984' #v3
joc_token_addr = '0x90700f190e4A6B271864E815370461b154e7Fb39'
infura_project_id = '8223a10124204e469b3d38ba19adfa12'
weth_token_addr = '0xc778417E063141139Fce010982780140Aa0cD5Ab'

class Uniswap:
    def __init__(
        self, token_addr=joc_token_addr, network_addr=f"https://ropsten.infura.io/v3/{infura_project_id}"
    ) -> None:
        # fac_abi = json.load(factory_abi)
        # exch_abi = json.load(exchange_abi)
        # print(fac_abi)
        f = open('abi.json')
        abi_objects = json.load(f)
        # factory_abi = abi_objects["factory_abi"]
        factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

        # print(factory_abi)
        exchange_abi = abi_objects["exchange_abi"]
        # print(exchange_abi)
        f.close()

        self.w3 = Web3(Web3.HTTPProvider(network_addr))

        self.factory_contract = self.w3.eth.contract(address=factory_addr, abi=factory_abi)

        # allPairsLength = self.factory_contract.functions.allPairsLength().call()
        # print(allPairsLength)

        pair_addr = self.factory_contract.functions.getPair(self.w3.toChecksumAddress(weth_token_addr), self.w3.toChecksumAddress(joc_token_addr )).call()
        # exchange_addr = self.factory_contract.functions.getExchange(token_addr).call()
        # print(exchange_addr)
        print(pair_addr)
        # self.exchange_contract = self.w3.eth.contract(address=exchange_addr, abi=exchange_abi)
        
        # self.exchange_contract.functions.getEthToTokenInputPrice(self.w3.toWei('1', 'Ether')).call()



if __name__ == '__main__':
    a = Uniswap()