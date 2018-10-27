''' User interaction script '''

import os
import array
import numpy as np
from pwmanager import enc_string, dec_bstr, gen_subkeys, cbn_subkeys

def main_configure():
    strs = np.loadtxt('csv/plain_passwords.csv', dtype=str, delimiter=',')
    print strs, '\n'

def test_encryption():
    n = 5
    keylen = 64

    ## generate random private key
    pk = array.array('B', os.urandom(keylen))

    ## test message
    msg = '!!@@##$$%%^^&&**(())//\\\\v98m21n1ycb27ehoaisejlv2'

    ## encrypt message
    estr = enc_string(msg, pk)

    ## split key into N subkeys of same length
    subk = gen_subkeys(pk, n)

    ## merge subkeys
    cbn = cbn_subkeys(subk)

    ## decrypt with merged keys
    dstr = dec_bstr(estr, cbn)

    assert dstr == msg, '@@ Test Encryption Failed!'
    print '[T] Test Encryption Passed.'


if __name__ == '__main__':

    test_encryption()

    main_configure()
