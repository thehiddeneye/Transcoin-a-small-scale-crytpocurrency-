from flask import Flask
from flask import request
import json 
import requests
import hashlib as hasher
import datetime as date 
node =Flask(__name__)

class Block:
    def __init__(self,index,timestamp,data,previous_hash):
        self.index =index
        self.timestamp =timestamp 
        self.data = data
        self.previous_hash = previous_hash
        self.hash =self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index)+str(self.timestamp)+str(self.data)+str(self.previous_hash))
        return sha.hexdigest()
 
def create_genesis_block():
    return Block(0,date.datetime.now(),{
        "proof-of-work": 9,
        "transactions":None
    },"0")

miner_address = "q3nfwerfd-random-miner-address-wefgcvgfvgf"

blockchain = []
blockchain.append(create_genesis_block())

this_nodes_transactions = []
peer_nodes = []

mining = True

@node.route('/txion',methods = ['POST'])
def transaction():
    new_txion =request.get_json()
    this_nodes_transactions.append(new_txion)

    print "New transaction "
    print "From:{}".format(new_txion['from'].encode('ascii','replace')) 
    print "To:{}".format(new_txion['to'].encode('ascii','replace'))
    print "AMOUNT:{}".format(new_txion['amount'])

    return "Transaction submitted successfully \n" 

@node.route('/blocks',methods = ['GET'])

def get_blocks():
    chain_to_send =blockchain

    for i in range(len(chain_to_send)):
        block =chain_to_send[i]
        block_index = str(block.index)
        block_timestamp =str(block.timestamp)
        block_data = str(block.data)
        block_hash = str(block.hash)

        chain_to_send[i] = {
            "index":block_index,
            "timestamp":block_timestamp,
            "data":block_data,
            "hash":block_hash

        }

    chain_to_send =json.dumps(chain_to_send)
    return chain_to_send

def find_new_chains():
    other_chains = []

    for node_url in peer_nodes:
        block =requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    longest_chain  = get_blocks()
    other_chains = find_new_chains()
    for chain in other_chains :
        if len(longest_chain)< len(chain):
            longest_chain =chain 

    blockchain = longest_chain

def proof_of_work(last_proof):
    incrementor =last_proof +1

    while not (incrementor%9== 0 and incrementor%last_proof==0):
        incrementor +=1
    return incrementor

@node.route('/mine',methods = ['GET'])
def mine():
    last_block =blockchain[len(blockchain)-1]
    last_proof = last_block.data['proof_of_work']
    
    proof = proof_of_work(last_proof)

    this_nodes_transactions.append({
        "from":"network",
        "to":miner_address,
        "amount":1
    })
    
    new_block_data = {
        "proof-of-work": proof,
        "transactions":list(this_nodes_transactions)
    }

    new_block_index = last_block.index+1 
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    this_nodes_transactions[:] = []
    mined_block =Block(new_block_index,new_block_timestamp,new_block_data ,last_block_hash)
    blockchain.append(mined_block)
    

    return json.dumps({
        "index":new_block_index,
        "timestamp":new_block_timestamp,
        "data":new_block_data,
        "hash":last_block_hash
    }) +"\n"

node.run()