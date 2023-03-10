# coding:utf-8
from bitcoin import *
import lib.common
from model import Model
from lib.common import pubkey_to_address
from database import AccountDB


def new_account():
    # private_key = lib.common.random_key()
    # public_key = lib.common.hash160(private_key.encode())
    private_key = random_key()
    public_key = lib.common.hash160(private_key.encode())
    address = pubtoaddr(privtopub(private_key))
    adb = AccountDB()
    adb.insert({'pubkey': public_key, 'address': address})
    return private_key, public_key, address


def get_account():
    adb = AccountDB()
    return adb.find_one()
