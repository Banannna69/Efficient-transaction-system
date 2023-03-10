from curses.ascii import NUL
from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, jsonify, request
from matplotlib import blocking_input
from numpy import block
from lib.common import cprint
from database import *
from account import *
import time
from miner import mine
from transaction import Transaction as trans
import hashlib
from aggregate import aggregate as aggre
from encrypt.sm3Hash import sm3Hash
import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
finally:
    s.close()


import json
app = Flask(__name__)

# route()方法用于设定路由；类似spring路由配置


@app.route('/')
def index():
    try:

        account = AccountDB()
        accounts = (account.read())
        accountlens = len(accounts)
        # 判断是否有用户存在
        try:
            currentAccount = accounts[0]['address']
        except:
            accountlens = 0
            currentAccount = None
        # 判断是否有交易存在
        if currentAccount != None:
            try:
                txlens = (len((TransactionDB().find_all())))
                tx = (TransactionDB().find_all())[-6:]
            except:
                txlens = 0
            # 判断是否有未确认的交易存在
            try:
                untx = UnTransactionDB().find_all()
                untxlens = (len(untx))
            except:
                untxlens = 0
            # 判断是否有区块存在
            try:
                blocks = BlockChainDB().find_all()
                blocklen = len(blocks)
            except:
                blocklen = 0

        else:
            tx = (TransactionDB().find_all())[0:0]
            txlens = 0
            untxlens = 0
            blocklen = 0

    except Exception as e:
        accountlens = 0

    return render_template('/index.html', lens=accountlens, output=accounts, currentAccount=currentAccount, txlens=txlens, blocklens=blocklen, untxlens=untxlens, tx=tx)


@app.route('/accounts')
def get_html():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    account = AccountDB()
    accounts = json.loads(account.read())
    return render_template('account.html', output=accounts)


@app.route('/create')
def createAccount():
    start = time.time()
    ac = new_account()
    end = time.time()
    print('账户创建成功\n', '花费时间为:', end-start)

    print(ac)
    # ac = [1, 2, 3]
    secKey = ac[0]
    pubKey = ac[1]
    address = ac[2]

    return render_template('/create.html', secKey=secKey, pubKey=pubKey, address=address)


@app.route('/mine')
def Mine():

    account = AccountDB()
    accounts = (account.read())
    # 判断是否有用户存在
    try:
        currentAccount = accounts[0]['address']
    except:
        currentAccount = None

    return render_template('/mine.html', currentAccount=currentAccount,)


@app.route('/mining')
def mining():
    # 挖矿
    start = time.time()
    mineInfo = mine().to_dict()
    end = time.time()
    print('挖到新区快\n', '花费时间为:', end-start)

    return render_template('/mineInfo.html', mineInfo=mineInfo)


utxo = {}


@app.route('/block')
def Block():
    account = AccountDB()
    accounts = (account.read())
    # 判断是否有用户存在
    try:
        currentAccount = accounts[0]['address']
    except:
        currentAccount = None

    try:
        block = BlockChainDB()
        blockList = ((block.find_all()))
        blocklen = len(blockList)

    except:
        blockList = None
        blocklen = 0
    return render_template('block.html', currentAccount=currentAccount, output=blockList, blocklen=blocklen)


@app.route('/transaction')
def Transaction():

    account = AccountDB()
    accounts = (account.read())
    # 判断是否有用户存在
    try:
        currentAccount = accounts[0]['address']
    except:
        currentAccount = None
    return render_template('/transaction.html', currentAccount=currentAccount, output=accounts)


@app.route('/transfer/<ToAccount>/<Amount>')
def Transfer(ToAccount, Amount):

    account = AccountDB()
    accounts = (account.read())
    # 判断是否有用户存在
    try:
        currentAccount = accounts[0]['address']
    except:
        currentAccount = None

    FromAddress = currentAccount

    try:

        if int(Amount) > 20:
            return "Amount too large"
        else:
            start = time.time()
            utxo = (trans.transfer(FromAddress, ToAccount, Amount))
            end = time.time()
            print('交易完成\n', '花费时间为:', end-start)
            return (utxo)
    except Exception as e:
        print(e)
        return "False"


@app.route('/crypto')
def crypto():
    sig_aggre = ''
    account = AccountDB()
    accounts = (account.read())
    # 判断是否有用户存在
    try:
        currentAccount = accounts[0]['address']
    except:
        currentAccount = None
    # 获取到单个签名值，聚合签名值，以及公钥
    try:
        pk_list = []
        signature = SignatureDB()
        signatures = (signature.read())
        sig_sum = len(signatures)
        sig_pk_list = signatures[0]['pk'].lstrip('(').rstrip(')').strip().split(',')

        for pk in sig_pk_list:
            pk = pk.strip()
            pk_list.append(pk)
        for data in signatures:
            temp = str(hashlib.md5(data['sig_hash'].encode()).hexdigest()).lower()
            sig_aggre = sig_aggre + temp
        aggre_result = str(hashlib.sha256(sig_aggre.encode()).hexdigest()).lower()
    except:
        signatures = ''
        sig_aggre = None
        aggre_result = ''
        pk_list = []

    # 验证签名值是否正确
    try:
        aggregate = AggregateDB()
        aggre_list = (aggregate.read())
        aggre_verify_data = str(hashlib.sha256(aggre_list[-1].encode()).hexdigest()).lower()
    except:
        aggre_verify_data = ''

    return render_template('/crypto.html', currentAccount=currentAccount, signatures=signatures, sig_sum=sig_sum,
                           aggre_result=aggre_result, pk_list=pk_list, aggre_verify_data=aggre_verify_data)


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5001, debug=False
    app.run(host="0.0.0.0", port=5001, debug=True)
