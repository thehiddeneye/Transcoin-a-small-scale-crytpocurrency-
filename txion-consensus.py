#consensus

@node.route('/route',methods=['GET'])

def get_blocks():
    chain_to_send =blockchain

    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp=str(block.timestamp)
        block_data=str(block.data)
        block_hash=str(block.hash)

        block ={
            "index":block_index,
            "timestamp":block_timestamp,
            "data":block_data,
            "hash":block_hash
        }

        chain_to_send =json.dumps(chain_to_send)
        return chain_to_send

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes :
        block =request.get(node_url +"/blocks").content
        block = json.loads(block)
        other_chains.append(block)

    return other_chains
def consensus():
    other_chains =find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest chain) <len(chain):
            longest_chain = chain
    
    blockchain =longest_chain