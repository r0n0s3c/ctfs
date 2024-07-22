from web3 import Web3
import os
import socket

def connect_and_send():
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect
    port = 40000  # replace with your port

    # connect to the server on local computer
    s.connect(('34.46.30.131', port))  # replace with your IP

    # receive data from the server
    data = s.recv(1024)

    # send a thank you message to the client.
    s.sendall(b'1\n')

    # receive data from the server
    data = s.recv(1024)

    # close the connection
    s.close()

    return repr(data)

data = connect_and_send().split("\\n")
contract_address =  ""
rpc_url = ""
private_key = ""
wallet_address = ""
contract_abi = [{"inputs":[{"internalType":"uint48","name":"amount","type":"uint48"}],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"getMoney","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"isChallSolved","outputs":[{"internalType":"bool","name":"solved","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint48","name":"amount","type":"uint48"}],"name":"loan","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint48","name":"amount","type":"uint48"}],"name":"withdraw","outputs":[],"stateMutability":"payable","type":"function"}]
for item in data:
    if 'contract address:' in item:
        contract_address = item.split(': ')[1]
    elif 'rpc-url:' in item:
        rpc_url = item.split(': ')[1]
    elif 'private-key:' in item:
        private_key = item.split(': ')[1]
    elif 'Wallet address:' in item:
        wallet_address = item.split(': ')[1]

print(f"contract_address: {contract_address}, rpc_url: {rpc_url}, private_key: {private_key}, wallet_address: {wallet_address}")

w3 = Web3(Web3.HTTPProvider(rpc_url))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def loan(amount):
    nonce = w3.eth.get_transaction_count(wallet_address)

    txn_dict = contract.functions.loan(amount).build_transaction({ "nonce": nonce, "from": wallet_address })

    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)

    result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(result)

    print(tx_receipt)

def withdraw(amount):
    nonce = w3.eth.get_transaction_count(wallet_address)

    txn_dict = contract.functions.withdraw(amount).build_transaction({ "nonce": nonce, "from": wallet_address })

    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)

    result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(result)

    print(tx_receipt)

def deposit(amount):
    nonce = w3.eth.get_transaction_count(wallet_address)

    txn_dict = contract.functions.deposit(amount).build_transaction({ "nonce": nonce, "from": wallet_address, "value": amount})

    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)

    result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(result)

    print(tx_receipt)


def ischallsolved():
    #nonce = w3.eth.get_transaction_count(wallet_address)

    txn_dict = contract.functions.isChallSolved().call()

    #signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)

    #result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    #tx_receipt = w3.eth.wait_for_transaction_receipt(result)

    print(txn_dict)

def getMoney():
    #nonce = w3.eth.get_transaction_count(wallet_address)

    txn_dict = contract.functions.getMoney().call()

    #signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)

    #result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    #tx_receipt = w3.eth.wait_for_transaction_receipt(result)

    print(txn_dict)

deposit(100)
#ischallsolved()
getMoney()
#withdraw(100)



# def get_money():
#     nonce = w3.eth.nonce = w3.eth.get_transaction_count(wallet_address)

#     txn_dict = contract.functions.getMoney().call()
#     print(txn_dict)

#     signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=private_key)

#     result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

#     tx_receipt = w3.eth.waitForTransactionReceipt(result)

#     print(tx_receipt)

# get_money()