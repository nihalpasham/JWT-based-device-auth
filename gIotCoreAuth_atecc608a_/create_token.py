
from base64 import base64
import utime
import ntptime, machine
import ujson
import ubinascii

# Set the esp32's real time clock. We'll need this to generate bearer (jwt) tokens that expire. 
def set_time():
    ntptime.settime()
    tm = utime.localtime()
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    print('current time: {}'.format(utime.localtime()))

# Generates a (valid) signed 'jwt' token needed to authenticate with Google IoT Core. Token is generated via an external cryptoauthentication 
# device (i.e. 'atecc608a'). Benefit - a high security 'device authentication' solution for as cheap as 0.50$. The private key used to sign our jwt is 
# generated and stored on the cryptoauth device and **never leaves** it.   
def create_token(project_id, token_ttl, device, slot):
    # atecc608a cryptoauth device has support for ECDSA-SHA256 signatures. 
    header = '{"typ":"JWT","alg":"ES256"}'

    # Epoch_offset is needed because micropython epoch is 2000-1-1 and unix is 1970-1-1. Adding 946684800 (30 years)
    epoch_offset = 946684800
    claims = {
                # The time that the token was issued at
                'iat': utime.time() + epoch_offset,
                # The time the token expires.
                'exp': utime.time() + epoch_offset + token_ttl,
                # The audience field should always be set to the GCP project id.
                'aud': project_id
            }
 
    payload = ujson.dumps(claims)
    #print('payload', payload)

    # Base64 encoding of data and a quick (but crude) way to safely URL encode all bytes. 
    token = base64.b64encode(header.encode('ascii')).replace(b'+', b'-').replace(b'/', b'_').replace(b'=', b'') + b'.'
    #print('token', token)
    token = token + base64.b64encode(payload.encode('ascii')).replace(b'+', b'-').replace(b'/', b'_').replace(b'=', b'')
    #print('token', token)

    # ES256 standard requires a sha-256 digest of the message to be ECDSA signed. Raw signature is 64 bytes in length. 
    digest = device.atcab_sha(token)[1:-2]
    #print("atcab_sha %r %r", token, hexlify(digest))
    signature = device.atcab_sign(slot, digest)[1:-2]
    #print("atcab_sign %r", hexlify(signature))

    # An additional step to verify the signature with the associated public key. This is just a sanity check. (can be 
    # excluded if you want to save some time or compute). 
    public_key = device.atcab_get_pubkey(slot)[1:-2]
    #print("atcab_get_pubkey %r", hexlify(public_key))
    verified = device.atcab_verify_extern(digest, signature, public_key)
    #print("atcab_verify_extern %r", verified)

    token = token + b'.' + ubinascii.b2a_base64(signature)[:-1].replace(b'+', b'-').replace(b'/', b'_').replace(b'=',b'')
    # A valid signed 'jwt' in ascii format. 
    jwt = token.decode('ascii')
    # print(jwt)
    return jwt




