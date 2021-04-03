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




if __name__ == '__main__':
        contract_abi = get_contract_abi_etherscan(contract_address)
        contract_decimals = w3.eth.contract(address=contract_address, abi=contract_abi).functions.decimals().call()
        contract_token_supply = w3.eth.contract(address=contract_address,
                                                abi=contract_abi).functions.totalSupply().call()
