import requests
import math

from web3 import Web3

# connecting to external eth node using HTTP + Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'))
connected = w3.isConnected()

etherscan_api_key = 'J5WK7PZUEN9IA3F8HTKY74FDVWD6IDQK7N'
wallet_address = '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE'
contract_address = '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e'

0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e
0x3c318baf84b8748a84cc0432c15c8c336bea2dba

contract_abi_endpoint = 'https://api.etherscan.io/api?module=contract&action=getabi&address=' + contract_address + '&apikey=' + etherscan_api_key


def get_contract_abi_etherscan(contract_address):
    result = requests.get(contract_abi_endpoint).json()["result"]
    return result


def get_contract_balance_for_wallet(contract_address, wallet_address):
    etherscan_token_balance_api = 'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=' + contract_address + '&address=' + wallet_address + '&tag=latest&apikey=' + etherscan_api_key
    token_balance = requests.get(etherscan_token_balance_api).json()["result"]
    return int(token_balance) / math.pow(10,18)


def get_eth_balance_for_wallet(wallet_address):
    address_balance_wei = w3.eth.get_balance(wallet_address)
    address_balance_ether = w3.fromWei(address_balance_wei, 'ether')
    return address_balance_ether


if __name__ == '__main__':
    if connected:
        print(f'Wallet Address', wallet_address)
        print(f'ETH Balance', get_eth_balance_for_wallet(wallet_address))
        contract_abi = get_contract_abi_etherscan(contract_address)
        # yfi_contract = w3.eth.contract(contract_address)
        print(f'Balance for contract ', contract_address, f' is ',
              get_contract_balance_for_wallet(contract_address, wallet_address))