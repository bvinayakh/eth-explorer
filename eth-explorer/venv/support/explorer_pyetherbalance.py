import pyetherbalance
# Sign up for https://infura.io/, and get the url to an ethereum node
infura_url = 'https://mainnet.infura.io/v3/3deb0847ce9942568005689574ba69db'
ethereum_address = '0xeb9f035dd1211af75976427d68d2d6dc549c458e'
# Create an pyetherbalance object , pass the infura_url
ethbalance = pyetherbalance.PyEtherBalance(infura_url)
# New token symbol
token = "OMG"
# Token details. The fields below are all required
details = {'symbol': 'OMG', 'address': '0xd26114cd6EE289AccF82350c8d8487fedB8A0C07', 'decimals': 18, 'name': 'OmiseGO'}
# Add token
erc20tokens = ethbalance.add_token(token, details)
# print list of all internal tokens
print(erc20tokens['HOT'])