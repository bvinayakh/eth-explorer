import json

from apikeys import *
from dbutils import *
from endpoints import *
from etherscan_functions import *
from utils import *
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(get_infura_endpoint() + get_infura_api_key()))


def get_transaction(_tx_hash):
    tx_hash_dict = dict(w3.eth.get_transaction(_tx_hash))
    tx_hash_json = json.loads(json.dumps(tx_hash_dict, cls=HexJsonEncoder))
    return tx_hash_json


# throw expected a bool, int, byte or bytearray in first arg, or keyword of hexstr or text at times, need to check later
def get_transaction_receipt(_tx_hash):
    tx_hash_dict = dict(w3.eth.getTransactionReceipt(_tx_hash))
    tx_hash_json = json.loads(json.dumps(tx_hash_dict, cls=HexJsonEncoder))
    return tx_hash_json


# need to fix the transfer amount to proper decimals
def decode_transaction__contract_details(_transaction):
    transaction_input = _transaction['input']
    if "0xa9059cbb" in transaction_input:
        try:
            contract_transfer = {}
            block_number = _transaction['blockNumber']
            contract_transfer['block'] = block_number
            transaction_hash = _transaction['hash']
            contract_transfer['txnhash'] = transaction_hash
            from_wallet_address = _transaction['from']
            contract_transfer['from'] = from_wallet_address
            contract_address = _transaction['to']
            contract_transfer['contract'] = contract_address
            transaction_input_without_method = str(transaction_input).replace("0xa9059cbb", "")
            transaction_input_to_address = '0x' + transaction_input_without_method[24:64]
            contract_transfer['to'] = transaction_input_to_address
            transaction_input_transfer_amount = transaction_input_without_method[64:128]
            contract_abi = get_contract_abi_etherscan(contract_address)
            # print(w3.eth.contract(address=contract_address, abi=contract_abi))
            contract_transfer['abi'] = contract_abi
            contract_decimals = w3.eth.contract(address=contract_address, abi=contract_abi).functions.decimals().call()
            contract_transfer['decimals'] = contract_decimals
            contract_token_supply = w3.eth.contract(address=contract_address,
                                                    abi=contract_abi).functions.totalSupply().call()
            contract_transfer['supply'] = contract_token_supply
            # base = int(contract_token_supply / 10 ** contract_decimals)
            # print('transfer amount ', int(transaction_input_transfer_amount, 16))
            # contract_transfer['amount'] = int(transaction_input_transfer_amount, 16)
            contract_transfer['amount'] = transaction_input_transfer_amount
            return contract_transfer
        except:
            print(f'Error in decode_transaction__contract_details for contract_address ', contract_address)
            pass
    else:
        return "No contracts in transaction"


def store_transaction_receipt(_transaction):
    try:
        sql = """insert into transaction_reciept("blockHash","blockNumber","contractAddress","cumulativeGasUsed","from","gasUsed",logs,"logsBloom","status","to","transactionHash","transactionIndex") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning "transactionHash"; """
        _blockHash = str(_transaction['blockHash'])
        _blockNumber = str(_transaction['blockNumber'])
        _contractAddress = str(_transaction['contractAddress'])
        _cumulativeGasUsed = str(_transaction['cumulativeGasUsed'])
        _from = str(_transaction['from'])
        _gasUsed = str(_transaction['gasUsed'])
        _logs = str(_transaction['logs'])
        _logsBloom = str(_transaction['logsBloom'])
        _status = str(_transaction['status'])
        _to = str(_transaction['to'])
        _transactionIndex = str(_transaction['transactionIndex'])
        _transactionHash = str(_transaction['transactionHash'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (
            _blockHash, _blockNumber, _contractAddress, _cumulativeGasUsed, _from, _gasUsed, _logs, _logsBloom, _status,
            _to, _transactionHash, _transactionIndex))
        _tx_hash = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return _tx_hash
    except:
        print(f'Error in store_transaction_receipt for transaction hash ', _transactionHash)
        pass




def store_transaction(_transaction):
    try:
        sql = """insert into transaction_information("blockHash","blockNumber","from",gas,"gasPrice",hash,input,nonce,r,s,"to","transactionIndex",v,"value") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning hash; """
        _blockHash = str(_transaction['blockHash'])
        _blockNumber = str(_transaction['blockNumber'])
        _from = str(_transaction['from'])
        _gas = str(_transaction['gas'])
        _gasPrice = str(_transaction['gasPrice'])
        _hash = str(_transaction['hash'])
        _input = str(_transaction['input'])
        _nonce = str(_transaction['nonce'])
        _r = str(_transaction['r'])
        _s = str(_transaction['s'])
        _to = str(_transaction['to'])
        _transactionIndex = str(_transaction['transactionIndex'])
        _v = str(_transaction['v'])
        _value = str(_transaction['value'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (
            _blockHash, _blockNumber, _from, _gas, _gasPrice, _hash, _input, _nonce, _r, _s, _to, _transactionIndex, _v,
            _value))
        _tx_hash = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return _tx_hash
    except:
        print(f'Error in store_transaction for transaction hash ',_hash)
        pass


