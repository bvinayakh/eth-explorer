import json

from web3 import Web3

# connecting to external eth node using HTTP + Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'))
connected = w3.isConnected()


if __name__ == '__main__':
    # print(f'Connect to Node',connected)

    latest_block_information: object = w3.eth.get_block('latest')
    latest_block_information_dict = json.loads(w3.toJSON(latest_block_information))
    print(latest_block_information_dict)
    #print(latest_block_information_dict.get('difficulty'))

    for value in latest_block_information_dict:
        print(value,f' == ',latest_block_information_dict.get(value))
