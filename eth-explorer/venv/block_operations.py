import json
from xml.etree.ElementPath import ops

from apikeys import get_infura_api_key
from dbutils import *
from endpoints import *
from utils import *
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(get_infura_endpoint() + get_infura_api_key()))


def get_block_information(_block_number):
    block_dict = dict(w3.eth.get_block(_block_number))
    block_json = json.loads(json.dumps(block_dict, cls=HexJsonEncoder))
    return block_json


def store_block(_block_information):
    try:
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
            _difficulty, _extraData, _gasLimit, _gasUsed, _hash, _logsBloom, _miner, _mixHash, _nonce, _number,
            _parentHash,
            _receiptsRoot, _sha3Uncles, _size, _stateRoot, _timestamp, _totalDifficulty, _transactions,
            _transactionsRoot,
            _uncles))
        _block_number = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return _block_number
    except OperationalError as opserror:
        print(f'DB Operational Error in store_block', opserror)
        pass
    except Exception as exception:
        print(f'Error in store_block', exception)
        pass
