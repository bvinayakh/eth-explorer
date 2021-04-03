# code will always get latest transactions from the blockchain and persist to db for analytics

from block_operations import *
from contract_operations import *
from transaction_operations import *

if __name__ == '__main__':
    # latest_block = get_block_information('latest')
    latest_block_number = get_block_information('latest')['number']
    if not block_exists(latest_block_number):
        # store latest_block to db
        for block_number in range(latest_block_number, latest_block_number - 100, -1):
            block_information = get_block_information(block_number)
            # store block_information to db
            print(block_information)
            block_number_db = store_block(block_information)
            print(f'stored block number ', block_number_db)
            for transaction in block_information['transactions']:
                try:
                    transaction = get_transaction(transaction)
                    # store transaction to db
                    tx_hash = store_transaction(transaction)
                    print(f'stored transaction hash ', tx_hash)
                    transaction_contract_details = decode_transaction__contract_details(transaction)
                    # store transaction_contract_details to db
                    print(transaction_contract_details)
                    if str(transaction_contract_details) != "No contracts in transaction":
                        _contract_address = store_contract_details(transaction_contract_details)
                        print(f'contract ', _contract_address, f' stored in db')
                    # always process transaction_receipt in the last because the transaction might be empty and could throw and error
                    transaction_receipt = get_transaction_receipt(transaction)
                    # store transaction_receipt to db
                    print(transaction_receipt)


                except TypeError as type_error:
                    print(f"Type Error Decoding ", type_error.args)
