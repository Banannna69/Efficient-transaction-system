import json
import hashlib
import time
# 对sig文件中的签名值进行聚合
def aggregate():
    sig_aggre = ''
    with open('./data/sig') as f:
        raw = f.readline()
    if len(raw) > 0:
        datas = json.loads(raw)
    else:
        datas = []
    sig_list_length = len(datas)
    print(sig_list_length)
    if (sig_list_length < 5):
        time.sleep(0.2)
    elif (sig_list_length < 10):
        time.sleep(0.7)
    elif (sig_list_length < 20):
        time.sleep(1.2)
    elif (sig_list_length < 30):
        time.sleep(1.7)
    elif (sig_list_length < 40):
        time.sleep(2.2)
    elif (sig_list_length < 50):
        time.sleep(2.7)
    elif (sig_list_length < 60):
        time.sleep(3.2)
    elif (sig_list_length < 70):
        time.sleep(3.7)
    elif (sig_list_length < 80):
        time.sleep(4.2)
    elif (sig_list_length < 90):
        time.sleep(4.7)
    else:
        time.sleep(5.2)

    for data in datas:
        temp = str(hashlib.md5(data['sig_hash'].encode()).hexdigest()).lower()
        sig_aggre = sig_aggre + temp

    result = str(hashlib.sha256(sig_aggre.encode()).hexdigest()).lower()
    return result
