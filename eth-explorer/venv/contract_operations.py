import json
from configparser import ConfigParser

import psycopg2
import requests
# from setuptools._distutils.command.config import config
from web3 import Web3


def get_contract_abi_etherscan(contract_address):
    result = requests.get(
        'https://api.etherscan.io/api?module=contract&action=getabi&address=' + contract_address + '&apikey=' + etherscan_api_key).json()[
        "result"]
    return result


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


def get_db_connection():
    conn = None
    try:
        params = config()
        # print('Connecting to the DB')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def get_decimals(contract_address, contract_abi):
    return w3.eth.contract(address=contract_address, abi=contract_abi).functions.decimals().call()


def get_total_supply():
    contract_token_supply = w3.eth.contract(address=contract_address, abi=contract_abi).functions.totalSupply().call()


def store_contract_details(_contract):
    # try:
        sql = """insert into contract_information("contract_block_number","contract_txn_hash","contract_address","contract_initiated_from","contract_sent_to","contract_amount","contract_decimals","contract_total_supply","contract_abi") values(%s,%s,%s,%s,%s,%s,%s,%s,%s) returning "contract_address"; """
        _block = str(_contract['block'])
        _txnhash = str(_contract['txnhash'])
        _from = str(_contract['from'])
        _to = str(_contract['to'])
        _abi = str(_contract['abi'])
        _decimals = str(_contract['decimals'])
        _supply = str(_contract['supply'])
        _amount = str(_contract['amount'])
        _contract = str(_contract['contract'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (_block, _txnhash, _contract, _from, _to, _amount, _decimals, _supply, _abi))
        _contract_address = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return _contract_address
    # except:
    #     print(f'Error in store_contract_details for contract ', _contract)
    #     pass


