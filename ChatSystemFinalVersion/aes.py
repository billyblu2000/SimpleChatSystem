# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES

#  bytes不是32的倍数那就补足为32的倍数
def add_to_32(value):
    while len(value) % 32 != 0:
            value += b'\x00'
    return value     # 返回bytes
 

# str转换为bytes超过32位时处理
def cut_value(org_str):
    org_bytes = str.encode(org_str)
    n = int(len(org_bytes) / 32)
    i = 0
    new_bytes = b''
    while n >= 1:
        i = i + 1
        new_byte = org_bytes[(i-1)*32:32*i-1]
        new_bytes += new_byte
        n = n - 1
    if len(org_bytes) % 32 == 0:                   # 如果是32的倍数，直接取值
        all_bytes = org_bytes
    elif len(org_bytes) % 32 != 0 and n>1:         # 如果不是32的倍数，每次截取32位相加，最后再加剩下的并补齐32位
        all_bytes = new_bytes + add_to_32 (org_bytes[i*32:])
    else:
        all_bytes = add_to_32 (org_bytes)          # 如果不是32的倍数，并且小于32位直接补齐
    return all_bytes
 

def AES_encrypt(org_str,key):
    aes = AES.new(cut_value(key), AES.MODE_ECB)
    encrypt_aes = aes.encrypt(cut_value(org_str))
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8') 
    return(encrypted_text)


def AES_decrypt(secret_str,key):
    aes = AES.new(cut_value(key), AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(secret_str.encode(encoding='utf-8'))
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return(decrypted_text)


if __name__ == '__main__':
    org_str = 'http://mp.weixin.qq.com/s?__biz=MjM5NjAxOTU4MA==&amp;mid=3009217590&amp;idx=1&amp;sn=14532c49bc8cb0817544181a10e9309f&amp;chksm=90460825a7318133e7905c02e708d5222abfea930e61b4216f15b7504e39734bcd41cfb0a26d&amp;scene=27#wechat_redirect'
    # 秘钥
    key = '123abc'
    secret_str = AES_encrypt(org_str,key)
    AES_decrypt(secret_str,key)
