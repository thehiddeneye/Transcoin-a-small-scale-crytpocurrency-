from flask import Flask
from flask import request

node = Flask(__name__)
#store the transactions this node has in a list

this_node_transactions = []

@node.route('/txion',methods =['POST'])
def transaction():
    if request.method == 'POST':
        #on each new post request we add the transaction to our list
        new_txion =request.get_json()
        #then we add transaction to our list 
        this_node_transactions.append(new_txion)
        print "new transaction "
        print "FROM:{}".format(new_txion['from'])
        print "TO:{}".format(new_txion['to'])
        print "AMOUNT :{}".format(new_txion['amount'])

        return "Transaction submission successful\n"

node.run()