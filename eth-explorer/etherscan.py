import requests

etherscan_api_key = 'J5WK7PZUEN9IA3F8HTKY74FDVWD6IDQK7N'
contract_address = '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e'
# etherscan_endpoint = 'https://api.etherscan.io/api?module=contract&action=getabi&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken'
# etherscan_endpoint = 'https://api.etherscan.io/api?module=contract&action=getabi&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey='+etherscan_api_key

contract_abi_endpoint='https://api.etherscan.io/api?module=contract&action=getabi&address='+contract_address+'&apikey='+etherscan_api_key
token_info_by_contract = 'https://api.etherscan.io/api?module=token&action=tokeninfo&contractaddress=' + contract_address + '&apikey=' + etherscan_api_key
etherscan_token_account_balance = 'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=' + contract_address + '&address=0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be&tag=latest&apikey=' + etherscan_api_key


etherscan_tx_receipt = 'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x6e5c379257246bc5db3774ea7bde2b706b5f1b3c491af33805931ef083aed2cb&apikey='+etherscan_api_key

if __name__ == '__main__':
    response = requests.get(etherscan_tx_receipt)
    print(response.json())
    # print(requests.get(contract_abi_endpoint).json())
