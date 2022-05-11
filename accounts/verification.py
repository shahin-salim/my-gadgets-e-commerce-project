import os
from twilio.rest import Client
from ecom.settings import  TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, services

# twillio send OTP function
def SendOTP(number):

    account_sid = os.environ['TWILIO_ACCOUNT_SID'] = TWILIO_ACCOUNT_SID
    auth_token = os.environ['TWILIO_AUTH_TOKEN'] = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    verification = client.verify \
                        .services(services) \
                        .verifications \
                        .create(to=number, channel='sms')
    print(verification.status)


# twillio verification of the otp
def check(otp, number):

    account_sid = os.environ['TWILIO_ACCOUNT_SID'] = TWILIO_ACCOUNT_SID
    auth_token = os.environ['TWILIO_AUTH_TOKEN'] =  TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    verification_check = client.verify \
                            .services(services) \
                            .verification_checks \
                            .create(to=number, code=otp)
    print(verification_check.status)
    print(verification_check)

    if verification_check.status ==  'approved':
        return True
    else:
        return False