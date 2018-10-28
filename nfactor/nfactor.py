''' User interaction script '''

import os
import array
import binascii
import numpy as np
from pwmanager import enc_string, dec_bstr, gen_subkeys, cbn_subkeys
from serialcomms import establish_conn, configure_requestnum

def main_configure():
#    strs = np.loadtxt('csv/plain_passwords.csv', dtype=str, delimiter=',')
#    print strs, '\n'

    ## setup hardware connection
    ser = establish_conn()
    num_factors = configure_requestnum(ser)
    print 'num: {}'.format(binascii.hexlify(num_factors))

    return

    ## test private key
    pk = array.array('B', 'drewcomeback')
    subk = gen_subkeys(pk, num_factors)

    ## send sub-keys to factors
    


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
