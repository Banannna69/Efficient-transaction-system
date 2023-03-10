# coding:utf-8
import json
import os

BASEDBPATH = 'data'
BLOCKFILE = 'blockchain'
TXFILE = 'tx'
UNTXFILE = 'untx'
ACCOUNTFILE = 'account'
NODEFILE = 'node'
SIGFILE = 'sig'
AGGREFILE = 'aggregate'


class BaseDB():

    filepath = ''

    def __init__(self):
        self.set_path()
        self.filepath = '/'.join((BASEDBPATH, self.filepath))

    def set_path(self):
        pass

    def find_all(self):
        return self.read()

    def insert(self, item):
        self.write(item)

    def read(self):
        raw = ''
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, 'r+') as f:
            raw = f.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []
        return data

    def write(self, item):
        data = self.read()
        if isinstance(item, list):
            data = data + item
        else:
            data.append(item)
        with open(self.filepath, 'w+') as f:
            f.write(json.dumps(data))
        return True

    def clear(self):
        with open(self.filepath, 'w+') as f:
            f.write('')

    def hash_insert(self, item):
        exists = False
        for i in self.find_all():
            if item['hash'] == i['hash']:
                exists = True
                break
        if not exists:
            self.write(item)


class NodeDB(BaseDB):

    def set_path(self):
        self.filepath = NODEFILE


class AccountDB(BaseDB):
    def set_path(self):
        self.filepath = ACCOUNTFILE

    def find_one(self):
        ac = self.read()
        return ac[0]


class BlockChainDB(BaseDB):

    def set_path(self):
        self.filepath = BLOCKFILE

    def last(self):
        bc = self.read()
        if len(bc) > 0:
            return bc[-1]
        else:
            return []

    def find(self, hash):
        one = {}
        for item in self.find_all():
            if item['hash'] == hash:
                one = item
                break
        return one

    def insert(self, item):
        self.hash_insert(item)


class TransactionDB(BaseDB):
    """
    Transactions that save with blockchain.
    """

    def set_path(self):
        self.filepath = TXFILE

    def find(self, hash):
        one = {}
        for item in self.find_all():
            if item['hash'] == hash:
                one = item
                break
        return one

    def insert(self, txs):
        if not isinstance(txs, list):
            txs = [txs]
        for tx in txs:
            self.hash_insert(tx)


class UnTransactionDB(TransactionDB):
    """
    Transactions that doesn't store in blockchain.
    """

    def set_path(self):
        self.filepath = UNTXFILE

    def all_hashes(self):
        hashes = []
        for item in self.find_all():
            hashes.append(item['hash'])
        return hashes

# 定义签名数据库类
class SignatureDB(BaseDB):
    def set_path(self):
        self.filepath = SIGFILE
    
    def insert(self, txs):
        if not isinstance(txs, list):
            txs = [txs]
        for tx in txs:
            self.hash_insert(tx)
            
class AggregateDB(BaseDB):
    def set_path(self):
        self.filepath = AGGREFILE
    def insert(self, item):
        if item != 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':
            raw = ''
            if not os.path.exists(self.filepath):
                return []
            with open(self.filepath, 'r+') as f:
                raw = f.readline()
            if len(raw) > 0:
                data = json.loads(raw)
            else:
                data = []
            
            if isinstance(item, list):
                data = data + item
            else:   
                data.append(item)
            with open(self.filepath, 'w+') as f:
                f.write(json.dumps(data))
        return True
