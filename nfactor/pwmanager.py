''' Manage password file encryption stuff '''

import os
import array
import numpy as np

def xor_ba(ba1, ba2):
    ba3 = ba1[:]
    for i in range(len(ba1)):
        ba3[i] ^= ba2[i]
    return ba3

def enc_string(s1, pk):
    bpk = pk*(1+len(s1)/len(pk))
    bstr = array.array('B', s1)
    bstr = xor_ba(bstr, bpk)
    return bstr

def dec_bstr(bstr, pk):
    bpk = pk*(1+len(bstr)/len(pk))
    bstr = xor_ba(bstr, bpk)
    sstr = ''.join([chr(b) for b in bstr])
    return sstr

def gen_subkeys(pk, n):
    res = []
    collective_xor = None
    for i in range(n-1):
        res.append(array.array('B', os.urandom(len(pk))))
        if collective_xor is None:
            collective_xor = res[-1][:]
        else:
            collective_xor = xor_ba(collective_xor, res[-1])
    collective_xor = xor_ba(collective_xor, pk)
    res.append(collective_xor)
    return res

def cbn_subkeys(subkeys):
    cbn = None
    for i in range(len(subkeys)):
        if cbn is None:
            cbn = subkeys[i]
        else:
            cbn = xor_ba(cbn, subkeys[i])
    return cbn
