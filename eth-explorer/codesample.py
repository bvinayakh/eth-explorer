import json
from hexbytes import HexBytes
from web3 import Web3

from hexbytes import HexBytes

# connecting to external eth node using HTTP + Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'))
connected = w3.isConnected()


# convert dict, attrdict to JSON
class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def get_tx_information(_tx_hash):
    tx_hash_dict = dict(w3.eth.get_transaction(_tx_hash))
    tx_hash_json = json.loads(json.dumps(tx_hash_dict, cls=HexJsonEncoder))
    return tx_hash_json


def get_transaction_receipt(_tx_hash):
    tx_hash_dict = dict(w3.eth.getTransactionReceipt(_tx_hash))
    tx_hash_json = json.loads(json.dumps(tx_hash_dict, cls=HexJsonEncoder))
    return tx_hash_json


if __name__ == '__main__':
    # latest_block_information: object = w3.eth.get_block('latest')
    # block_dict = dict(latest_block_information)
    # block_json = json.dumps(block_dict, cls=HexJsonEncoder)
    tx_hash_output = get_tx_information('0x6e5c379257246bc5db3774ea7bde2b706b5f1b3c491af33805931ef083aed2cb');
    print(tx_hash_output)
    print(tx_hash_output['hash'])
    tx_receipt = get_transaction_receipt(tx_hash_output['hash'])
    # print(tx_receipt)