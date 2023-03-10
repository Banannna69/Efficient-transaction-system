# coding:utf-8
from block import Block
import time
from transaction import Vout, Transaction
from account import get_account
from database import BlockChainDB, TransactionDB, UnTransactionDB, SignatureDB, AggregateDB
from lib.common import unlock_sig, lock_sig
from aggregate import aggregate

MAX_COIN = 21000000
REWARD = 20

def reward():
    reward = Vout(get_account()['address'], REWARD)
    tx = Transaction([], reward)
    return tx

def coinbase():
    """
    First block generate.
    """
    rw = reward()
    cb = Block(0, int(time.time()), [rw.hash], "")
    nouce = cb.pow()
    cb.make(nouce)
    # Save block and transactions to database.
    BlockChainDB().insert(cb.to_dict())
    TransactionDB().insert(rw.to_dict())
    return cb

def get_all_untransactions():
    UnTransactionDB().all_hashes()

def mine():
    """
    Main miner method.
    """
    # Found last block and unchecked transactions.
    last_block = BlockChainDB().last()
    if len(last_block) == 0:
        last_block = coinbase().to_dict()
    untxdb = UnTransactionDB()
    sigdb = SignatureDB()
    # Miner reward
    rw = reward()
    untxs = untxdb.find_all()
    untxs.append(rw.to_dict())
    # untxs_dict = [untx.to_dict() for untx in untxs]
    untx_hashes = untxdb.all_hashes()
    # 对签名进行聚合
    start_time = time.time()
    print(str(start_time))
    result = aggregate()
    end_time = time.time()
    print(str(end_time))
    print("生成聚合签名" + "\n" + "花费时间为：" + str(end_time - start_time))
    # 将聚合后的结果写入aggregate文件
    AggregateDB().insert(result)
    # 清除sig文件里的内容
    sigdb.clear()
    # Clear the untransaction database.
    untxdb.clear()
    # Miner reward is the first transaction.
    untx_hashes.insert(0,rw.hash)
    cb = Block( last_block['index'] + 1, int(time.time()), untx_hashes, last_block['hash'])
    nouce = cb.pow()
    cb.make(nouce)
    # Save block and transactions to database.
    BlockChainDB().insert(cb.to_dict())
    TransactionDB().insert(untxs)
    # Broadcast to other nodes
    Block.spread(cb.to_dict())
    Transaction.blocked_spread(untxs)
    return cb