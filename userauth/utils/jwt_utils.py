import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_tokens(user):
    access_payload = {
        "user_id": str(user.id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_SETTINGS['ACCESS_TOKEN_LIFETIME']),
        "type": "access",
        "iat": datetime.utcnow(),
    }
    access_token = jwt.encode(access_payload, settings.JWT_SETTINGS['SECRET_KEY'], algorithm=settings.JWT_SETTINGS['ALGORITHM'])

    refresh_payload = {
        "user_id": str(user.id),
        "exp": datetime.utcnow() + timedelta(days=settings.JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']),
        "type": "refresh",
        "iat": datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SETTINGS['SECRET_KEY'], algorithm=settings.JWT_SETTINGS['ALGORITHM'])

    return access_token, refresh_token

def decode_token(token, allow_expired=False):
    options = {"verify_exp": not allow_expired}
    payload = jwt.decode(
        token,
        settings.JWT_SETTINGS['SECRET_KEY'],
        algorithms=[settings.JWT_SETTINGS['ALGORITHM']],
        options=options
    )
    return payload

