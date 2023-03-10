# coding:utf-8
import json
import time
import hashlib
from database import SignatureDB
from encrypt import sm9
from account import get_account


def sig():
    with open('./data/untx') as f:
        raw = f.readline()
    if len(raw) > 0:
        datas = json.loads(raw)
    else:
        datas = []

    msg = str(datas[-1]['timestamp']) + str(datas[-1]['vout'][-1]['amount'])
    account_dict = get_account()
    identity = account_dict['address']
    # 初始化
    mpk, secret = sm9.setup('sign')
    Da = sm9.private_key_extract('sign', mpk, secret, identity)
    Q = sm9.public_key_extract('sign', mpk, identity)
    sign_start_time = time.time()
    sig_res = sm9.sign(mpk, Da, msg)
    sign_end_time = time.time()
    print("生成签名" + "\n" + "花费时间为：" + str(sign_end_time - sign_start_time))

    # verify_start_time = time.time()
    result = sm9.verify(mpk, identity, msg, sig_res)
    # verify_end_time = time.time()
    # print("验证签名" + "\n" + "花费时间为：" + str(verify_end_time - verify_start_time))

    datas[-1]['msg'] = msg
    datas[-1]['pk'] = str(Q)
    datas[-1]['sk'] = str(Da)
    datas[-1]['mpk'] = str(mpk)
    datas[-1]['sig'] = str(sig_res)
    datas[-1]['sig_hash'] = str(hashlib.sha256(datas[-1]['sig'].encode()).hexdigest()).lower()
    # 验证签名是否正确
    if result:
        datas[-1]['result'] = 'Verification succeeded'
    else:
        datas[-1]['result'] = 'verification failed'

    # 写入data文件中
    SignatureDB().insert(datas[-1])

    # 对每一个没有确认的交易进行确认
    # for data in datas:
    #     msg = str(data['timestamp']) + str(data['vout'][0]['amount'])
    #     account_dict = get_account()
    #     identity = account_dict['address']
    #     # 初始化
    #     mpk, secret = sm9.setup('sign')
    #     Da = sm9.private_key_extract('sign', mpk, secret, identity)
    #     Q = sm9.public_key_extract('sign', mpk, identity)

    #     sign_start_time = time.time()
    #     sig_res = sm9.sign(mpk, Da, msg)
    #     sign_end_time = time.time()
    #     print("生成签名" + "\n" + "花费时间为：" + str(sign_end_time - sign_start_time))

    #     # verify_start_time = time.time()
    #     result = sm9.verify(mpk, identity, msg, sig_res)
    #     # verify_end_time = time.time()
    #     # print("验证签名" + "\n" + "花费时间为：" + str(verify_end_time - verify_start_time))

    #     data['msg'] = msg
    #     data['pk'] = str(Q)
    #     data['sk'] = str(Da)
    #     data['mpk'] = str(mpk)
    #     data['sig'] = str(sig_res)
    #     data['sig_hash'] = str(hashlib.sha256(data['sig'].encode()).hexdigest()).lower()
    #     # 验证签名是否正确
    #     if result:
    #         data['result'] = 'Verification succeeded'
    #     else:
    #         data['result'] = 'verification failed'

    #     # 写入data文件中
    #     SignatureDB().insert(data)
