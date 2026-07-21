from django.core.signing import TimestampSigner

SC003_VERIFICATION_SALT = 'sc003-2step-verification'

def generate_verification_token(user_id):
    signer = TimestampSigner(salt=SC003_VERIFICATION_SALT)
    return signer.sign_object({
        'user_id': user_id,
        'purpose': 'otp_verification'
    })

def mask_phone_number(phone_number):
    if not phone_number or len(phone_number) < 4:
        return None
    return "******" + phone_number[-4:]
