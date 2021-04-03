import json
from configparser import ConfigParser

import psycopg2
import requests
from setuptools._distutils.command.config import config
from web3 import Web3

etherscan_api_key = 'J5WK7PZUEN9IA3F8HTKY74FDVWD6IDQK7N'
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'))




def get_contract_transactions():
    sql = """select "blockNumber","hash","from","to","input" from transaction_information where "input" LIKE '0xa9059cbb%' order by "blockNumber" DESC"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    _contract_transactions = cursor.fetchall()
    conn.commit()
    cursor.close()
    return _contract_transactions