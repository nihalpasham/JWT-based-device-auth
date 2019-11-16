import ubinascii
from cryptoauthlib.device import ATECCX08A

device = ATECCX08A()
#print(device)

public_key = bytearray(64)
public_key = device.atcab_get_pubkey(2)
print(ubinascii.hexlify(public_key.response_data[1:-2]))

# Convert to the key to PEM format
public_key_pem = ubinascii.unhexlify('3059301306072A8648CE3D020106082A8648CE3D03010703420004') + public_key.response_data[1:-2]
public_key_pem = '-----BEGIN PUBLIC KEY-----\n' + ubinascii.b2a_base64(public_key_pem).decode('ascii') + '\n-----END PUBLIC KEY-----'

print(public_key_pem)