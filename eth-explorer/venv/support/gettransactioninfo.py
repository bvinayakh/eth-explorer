import json
from configparser import ConfigParser

import psycopg2
import requests
from setuptools._distutils.command.config import config
from web3 import Web3

etherscan_api_key = 'J5WK7PZUEN9IA3F8HTKY74FDVWD6IDQK7N'
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'))


def get_contract_abi_etherscan(contract_address):
    result = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address=' + contract_address + '&apikey=' + etherscan_api_key).json()["result"]
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


def get_contract_transactions():
    sql = """select "blockNumber","hash","from","to","input" from transaction_information where "input" LIKE '0xa9059cbb%' order by "blockNumber" DESC"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    _contract_transactions = cursor.fetchall()
    conn.commit()
    cursor.close()
    return _contract_transactions


if __name__ == '__main__':
    #get transaction information from DB
    print(f'Contract Transactions')
    transactions_list = get_contract_transactions()
    for transaction_detail in transactions_list:
        block_number = transaction_detail[0]
        transaction_hash = transaction_detail[1]
        from_wallet_address = transaction_detail[2]
        contract_address = transaction_detail[3]
        transaction_input = transaction_detail[4]

        print(f'transaction hash ',transaction_hash)
        print(f'contract address', contract_address)
        print(f'from wallet ', from_wallet_address)
        # print(transaction_input)
        transaction_input_without_method = str(transaction_input).replace("0xa9059cbb","")
        # print(transaction_input_without_method)
        transaction_input_to_address='0x'+transaction_input_without_method[24:64]
        print(transaction_input_to_address)
        transaction_input_transfer_amount=transaction_input_without_method[64:128]
        print(transaction_input_transfer_amount)
        contract_abi = get_contract_abi_etherscan(contract_address)
        # print(w3.eth.contract(address=contract_address, abi=contract_abi))
        contract_decimals = w3.eth.contract(address=contract_address, abi=contract_abi).functions.decimals().call()
        contract_token_supply = w3.eth.contract(address=contract_address, abi=contract_abi).functions.totalSupply().call()
        base = int(contract_token_supply / 10 ** contract_decimals)
        print(f'base ',base)
        print('transfer amount ',int(transaction_input_transfer_amount,16))
        print(' ')
