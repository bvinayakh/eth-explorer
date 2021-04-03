import json
from configparser import ConfigParser

import psycopg2
import requests
from hexbytes import HexBytes
from web3 import Web3

# connecting to external eth node using HTTP + Infura
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'))
connected = w3.isConnected()


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def get_db_connection():
    conn = None
    try:
        params = config()
        # print('Connecting to the DB')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


# def get_block_information(_block_number):
#     block_dict = dict(w3.eth.get_block(_block_number))
#     block_json = json.loads(json.dumps(block_dict, cls=HexJsonEncoder))
#     return block_json


def get_tx_information(_tx_hash):
    tx_hash_dict = dict(w3.eth.get_transaction(_tx_hash))
    tx_hash_json = json.loads(json.dumps(tx_hash_dict, cls=HexJsonEncoder))
    return tx_hash_json


# def get_block_information_etherscan(_block_number):
#     endpoint = 'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag=0x10d4f&boolean=true&apikey=' + etherscan_api_key
#     return requests.get(endpoint).json()


def get_transaction_reciept(_tx_hash):
    tx_hash_dict = dict(w3.eth.getTransactionReceipt(_tx_hash))
    tx_hash_json = json.loads(json.dumps(tx_hash_dict, cls=HexJsonEncoder))
    return tx_hash_json


def store_block(_block_information):
    sql = """insert into block_information(difficulty,"extraData","gasLimit","gasUsed",hash,"logsBloom",miner,"mixHash",nonce,"number","parentHash","receiptsRoot","sha3Uncles","size","stateRoot","timestamp","totalDifficulty",transactions,"transactionsRoot",uncles) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning number;"""
    _difficulty = str(_block_information['difficulty'])
    _extraData = str(_block_information['extraData'])
    _gasLimit = str(_block_information['gasLimit'])
    _gasUsed = str(_block_information['gasUsed'])
    _hash = str(_block_information['hash'])
    _logsBloom = str(_block_information['logsBloom'])
    _miner = str(_block_information['miner'])
    _mixHash = str(_block_information['mixHash'])
    _nonce = str(_block_information['nonce'])
    _number = str(_block_information['number'])
    _parentHash = str(_block_information['parentHash'])
    _receiptsRoot = str(_block_information['receiptsRoot'])
    _sha3Uncles = str(_block_information['sha3Uncles'])
    _size = str(_block_information['size'])
    _stateRoot = str(_block_information['stateRoot'])
    _timestamp = str(_block_information['timestamp'])
    _totalDifficulty = str(_block_information['totalDifficulty'])
    # transactions is a list, converting it to string for storing in DB
    _transactions_str = ""
    for _transactions_str in _block_information['transactions']:
        _transactions_str += _transactions_str + ","
    _transactions = _transactions_str
    _transactionsRoot = _block_information['transactionsRoot']
    _uncles_str = ""
    for _uncles_str in _block_information['uncles']:
        _uncles_str += _uncles_str + ","
    _uncles = _uncles_str

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (
        _difficulty, _extraData, _gasLimit, _gasUsed, _hash, _logsBloom, _miner, _mixHash, _nonce, _number, _parentHash,
        _receiptsRoot, _sha3Uncles, _size, _stateRoot, _timestamp, _totalDifficulty, _transactions, _transactionsRoot,
        _uncles))
    _block_number = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return _block_number


def store_transaction(_tx_hash):
    sql = """insert into transaction_information("blockHash","blockNumber","from",gas,"gasPrice",hash,input,nonce,r,s,"to","transactionIndex",v,"value") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning hash; """
    _blockHash = str(_tx_hash['blockHash'])
    _blockNumber = str(_tx_hash['blockNumber'])
    _from = str(_tx_hash['from'])
    _gas = str(_tx_hash['gas'])
    _gasPrice = str(_tx_hash['gasPrice'])
    _hash = str(_tx_hash['hash'])
    _input = str(_tx_hash['input'])
    _nonce = str(_tx_hash['nonce'])
    _r = str(_tx_hash['r'])
    _s = str(_tx_hash['s'])
    _to = str(_tx_hash['to'])
    _transactionIndex = str(_tx_hash['transactionIndex'])
    _v = str(_tx_hash['v'])
    _value = str(_tx_hash['value'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (
        _blockHash, _blockNumber, _from, _gas, _gasPrice, _hash, _input, _nonce, _r, _s, _to, _transactionIndex, _v,
        _value))
    _tx_hash = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return _tx_hash


def store_transaction_receipt(_tx_hash_reciept):
    sql = """insert into transaction_reciept("blockHash","blockNumber","contractAddress","cumulativeGasUsed","from","gasUsed",logs,"logsBloom","status","to","transactionHash","transactionIndex") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning "transactionHash"; """
    _blockHash = str(_tx_hash_reciept['blockHash'])
    _blockNumber = str(_tx_hash_reciept['blockNumber'])
    _contractAddress = str(_tx_hash_reciept['contractAddress'])
    _cumulativeGasUsed = str(_tx_hash_reciept['cumulativeGasUsed'])
    _from = str(_tx_hash_reciept['from'])
    _gasUsed = str(_tx_hash_reciept['gasUsed'])
    _logs = str(_tx_hash_reciept['logs'])
    _logsBloom = str(_tx_hash_reciept['logsBloom'])
    _status = str(_tx_hash_reciept['status'])
    _to = str(_tx_hash_reciept['to'])
    _transactionIndex = str(_tx_hash_reciept['transactionIndex'])
    _transactionHash = str(_tx_hash_reciept['transactionHash'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (
        _blockHash, _blockNumber, _contractAddress, _cumulativeGasUsed, _from, _gasUsed, _logs, _logsBloom, _status,
        _to, _transactionHash, _transactionIndex))
    _tx_hash = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return _tx_hash


if __name__ == '__main__':
    if connected:
        # connect()
        latest_block_number = get_block_information('latest')['number']
        for block_number in range(latest_block_number, latest_block_number - 100, -1):
            block_information = get_block_information(block_number)
            # print(f'Block:', block_number, f' ', block_information)
            print(f'Block Number ', store_block(block_information), f' stored')
            transactions_list = block_information['transactions']
            try:
                for tx_hash in transactions_list:
                    # print(f'Transaction Hash ', tx_hash, " ", get_tx_information(tx_hash))
                    tx_hash_output = get_tx_information(tx_hash);
                    print(f'Transaction Hash ', store_transaction(tx_hash_output), f' stored')
                    tx_hash_receipt = get_transaction_reciept(tx_hash)
                    print(f'Transaction Receipt ', store_transaction_receipt(tx_hash_receipt), f' stored')
                print(f' ')
            except TypeError as type_error:
                print(f'TypeError ',type_error)
                pass
            except Error as e:
                print(f'Error ',e)
                pass
