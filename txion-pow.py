# ...blockchain
#...block class defintion

miner_address = "qweree123-random-miner-address-34345erfgbgghn"

def proof_of_work(last_proof):
    incrementor =last_proof +1

    while not(incrementor%9 == 0 and incrementor%last_proof == 0):
        incrementor +=1

    return incrementor

@node.route('/mine',methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain)-1]
    last_proof = last_block.data['proof-of-work']
    proof_of_work(last_proof)

    this_nodes_transactions.append(
        {"from":"network","to":miner_address ,"amount":1}
    )

    new_block_data = {
        "proof_of_work":proof,
        "transactions":list(this_nodes_transactions)
    }

    new_block_index = lsst_block.index+1
    new_block_timestamp = this_timestamp = date.datetime.now()
    new_block_hash = last_block.hash 
    
    this_nodes_transactions[:] = []
    
    mined_block = Block(new_block_index,new_block_timestamp,new_block_data ,new_block_hash)

    blockchain.append(mined_block)

    return json.dumps({
        "index":new_block_index,
        "timestamp":new_block_timestamp,
        "data":new_block_data,
        "hash":new_block_hash
    }) +"\n"
    


