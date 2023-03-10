import sys
from gmssl import sm2
from base64 import b64encode, b64decode
# sm2的公私钥
SM2_PRIVATE_KEY = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
SM2_PUBLIC_KEY = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)

# sm2加密
def encryptSm2(info):
    encode_info = sm2_crypt.encrypt(info.encode(encoding="utf-8"))
    encode_info = b64encode(encode_info).decode()  # 将二进制bytes通过base64编码
    return encode_info

# sm3解密
def decryptSm2(info):
    decode_info = b64decode(info.encode())  # 通过base64解码成二进制bytes
    decode_info = sm2_crypt.decrypt(decode_info).decode(encoding="utf-8")
    return decode_info
