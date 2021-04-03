import requests

from apikeys import *
from endpoints import *


def get_contract_abi_etherscan(contract_address):
    request_query = get_etherscan_endpoint() + '?module=contract&action=getabi&address=' + contract_address + '&apikey=' + get_etherscan_api_key()
    result = requests.get(request_query).json()["result"]
    return result
