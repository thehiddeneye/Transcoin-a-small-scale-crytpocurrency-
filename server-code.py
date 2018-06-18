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
