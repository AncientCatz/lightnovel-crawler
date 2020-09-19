# -*- coding: utf-8 -*-
import os
import pyotp

def otpSecretKey():
    secret_key = pyotp.random_base32()
    return secret_key
# end def

def otpURI():
    key = os.getenv('OTP_SECRET_KEY', '')
    if key == None:
       totp_uri = "Secret key not configured"
    else:
        totp_uri = pyotp.totp.TOTP(key).provisioning_uri(
            "admin@ancientcatz.eu.org",
            issuer_name="Lightnovel Crawler")
    # end if
    return totp_uri
# end def

def otpCode():
    key = os.getenv('OTP_SECRET_KEY', '')
    if key == None:
        pyotp_now = "Secret key not configured"
    else:
        totp = pyotp.TOTP(key)
        pyotp_now = totp.now()
    # end if
    return pyotp_now
# end def

def otpVerify(otp):
    key = os.getenv('OTP_SECRET_KEY', '')
    if key == None:
        pyotp_verify = False
    else:
        totp = pyotp.TOTP(key)
        pyotp_verify = totp.verify(your_code)
    # end if
    return pyotp_verify
# end def